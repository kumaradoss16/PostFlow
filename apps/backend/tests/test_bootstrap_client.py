"""Tests for backend bootstrap handshake client and transport."""

import ctypes
import json
import secrets
import sys
from ctypes import wintypes

import pytest

from postflow.bootstrap.client import (
    INVALID_HANDLE_VALUE,
    SocketOrMockTransport,
    WindowsNamedPipeTransport,
    get_transport,
    is_windows_named_pipe_path,
    run_bootstrap_handshake,
)
from postflow.middleware.auth_barrier import AuthBarrierState


class MockPipeTransport:
    """In-memory mock transport simulating supervisor pipe communication."""

    def __init__(self, supervisor_steps: list[dict[str, object]]) -> None:
        self.supervisor_steps = supervisor_steps
        self.step_idx = 0
        self.client_sent: list[dict[str, object]] = []
        self.connected = False
        self.closed = False

    def connect(self) -> None:
        self.connected = True

    def send_line(self, line: str) -> None:
        self.client_sent.append(json.loads(line))

    def read_line(self) -> str:
        if self.step_idx >= len(self.supervisor_steps):
            raise EOFError("No more mock messages from supervisor")
        msg = self.supervisor_steps[self.step_idx]
        self.step_idx += 1
        return json.dumps(msg)

    def close(self) -> None:
        self.closed = True


# =========================================================================
# F1: Transport selection prefix tests
# =========================================================================


def test_is_windows_named_pipe_path_valid() -> None:
    """Verify valid Windows named pipe path patterns return True."""
    assert is_windows_named_pipe_path(
        r"\\.\pipe\postflow-bootstrap-12345678-1234-1234-1234-123456789abc"
    )
    assert is_windows_named_pipe_path(r"\\.\pipe\my_pipe_001")
    assert is_windows_named_pipe_path(r"\\.\PIPE\case_insensitive_test")


def test_is_windows_named_pipe_path_invalid() -> None:
    """Verify invalid, malformed, or non-pipe paths return False."""
    # Extra trailing backslash
    assert not is_windows_named_pipe_path(r"\\.\pipe\\malformed")
    # Empty pipe name
    assert not is_windows_named_pipe_path("\\\\.\\pipe\\")
    assert not is_windows_named_pipe_path(r"\\.\pipe")
    # Traversal or invalid slashes
    assert not is_windows_named_pipe_path(r"\\.\pipe\sub/pipe")
    assert not is_windows_named_pipe_path(r"\\.\pipe\sub\pipe")
    assert not is_windows_named_pipe_path(r"\\.\pipe\..\traversal")
    # Socket or IP addresses
    assert not is_windows_named_pipe_path("127.0.0.1:8000")
    assert not is_windows_named_pipe_path("/tmp/postflow.sock")
    assert not is_windows_named_pipe_path("http://localhost:8000")
    # Non-strings
    assert not is_windows_named_pipe_path(None)  # type: ignore[arg-type]
    assert not is_windows_named_pipe_path(12345)  # type: ignore[arg-type]


def test_get_transport_class_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify get_transport returns the expected transport class based on path and OS."""
    monkeypatch.setattr(sys, "platform", "win32")

    valid_pipe = r"\\.\pipe\postflow-bootstrap-abc"
    assert isinstance(get_transport(valid_pipe), WindowsNamedPipeTransport)

    malformed_pipe = r"\\.\pipe\\malformed"
    assert isinstance(get_transport(malformed_pipe), SocketOrMockTransport)

    socket_path = "127.0.0.1:8000"
    assert isinstance(get_transport(socket_path), SocketOrMockTransport)


# =========================================================================
# F2: 64-bit Windows ctypes declarations & handle lifecycle tests
# =========================================================================


@pytest.mark.skipif(sys.platform != "win32", reason="Windows ctypes tests require Windows")
def test_windows_ctypes_function_signatures() -> None:
    """Verify that ctypes function prototypes are explicitly declared with pointer-sized types."""
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

    assert kernel32.CreateFileW.restype == wintypes.HANDLE
    assert kernel32.CreateFileW.argtypes is not None
    assert len(kernel32.CreateFileW.argtypes) == 7

    assert kernel32.ReadFile.restype == wintypes.BOOL
    assert kernel32.ReadFile.argtypes is not None
    assert len(kernel32.ReadFile.argtypes) == 5

    assert kernel32.WriteFile.restype == wintypes.BOOL
    assert kernel32.WriteFile.argtypes is not None
    assert len(kernel32.WriteFile.argtypes) == 5

    assert kernel32.CloseHandle.restype == wintypes.BOOL
    assert kernel32.CloseHandle.argtypes == [wintypes.HANDLE]

    assert kernel32.WaitNamedPipeW.restype == wintypes.BOOL
    assert kernel32.WaitNamedPipeW.argtypes == [wintypes.LPCWSTR, wintypes.DWORD]

    # Pointer size check
    assert ctypes.sizeof(wintypes.HANDLE) == ctypes.sizeof(ctypes.c_void_p)


def test_windows_transport_close_idempotent() -> None:
    """Verify transport close() is idempotent and does not perform double-close."""
    transport = WindowsNamedPipeTransport(r"\\.\pipe\test")
    # Should not raise when handle is None
    transport.close()
    assert transport._handle is None

    # Should not close invalid handles
    transport._handle = INVALID_HANDLE_VALUE
    transport.close()
    assert transport._handle is None

    transport._handle = 0
    transport.close()
    assert transport._handle is None


# =========================================================================
# F3: Startup race, bounded retry, and timeout tests
# =========================================================================


def test_windows_named_pipe_connect_retry_and_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify bounded connection retry on transient pipe not found and eventual timeout."""
    if sys.platform != "win32":
        pytest.skip("Requires Windows")

    transport = WindowsNamedPipeTransport(r"\\.\pipe\test")
    call_count = 0

    class MockKernel32:
        def CreateFileW(self, *args: object) -> object:
            nonlocal call_count
            call_count += 1
            return INVALID_HANDLE_VALUE

        def GetLastError(self) -> int:
            return 2  # ERROR_FILE_NOT_FOUND

    monkeypatch.setattr(ctypes.windll, "kernel32", MockKernel32())

    with pytest.raises(ConnectionError, match="Timed out after 0.1s connecting"):
        transport.connect(timeout_seconds=0.1)

    assert call_count >= 1
    assert transport._handle is None


def test_windows_named_pipe_connect_immediate_fail_on_access_denied(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify non-transient error (e.g. ERROR_ACCESS_DENIED) fails immediately without retry."""
    if sys.platform != "win32":
        pytest.skip("Requires Windows")

    transport = WindowsNamedPipeTransport(r"\\.\pipe\test")
    call_count = 0

    class MockKernel32:
        def CreateFileW(self, *args: object) -> object:
            nonlocal call_count
            call_count += 1
            return INVALID_HANDLE_VALUE

        def GetLastError(self) -> int:
            return 5  # ERROR_ACCESS_DENIED

    monkeypatch.setattr(ctypes.windll, "kernel32", MockKernel32())

    with pytest.raises(ConnectionError, match="error: 5"):
        transport.connect(timeout_seconds=5.0)

    assert call_count == 1
    assert transport._handle is None


# =========================================================================
# Protocol Handshake Tests
# =========================================================================


def test_handshake_successful(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify standard bootstrap handshake succeeds and activates barrier."""
    barrier_state = AuthBarrierState(initially_active=False)
    challenge = secrets.token_hex(32)
    auth_token = secrets.token_hex(32)

    mock_transport = MockPipeTransport([])

    def mock_get_transport(_path: str) -> MockPipeTransport:
        return mock_transport

    monkeypatch.setattr("postflow.bootstrap.client.get_transport", mock_get_transport)

    def dynamic_read_line() -> str:
        if mock_transport.step_idx == 0:
            mock_transport.step_idx += 1
            return json.dumps(
                {
                    "protocol_version": 1,
                    "challenge_nonce": challenge,
                }
            )
        if mock_transport.step_idx == 1:
            mock_transport.step_idx += 1
            backend_ready = mock_transport.client_sent[0]
            backend_nonce = backend_ready["backend_nonce"]
            return json.dumps(
                {
                    "auth_token": auth_token,
                    "backend_nonce_ack": backend_nonce,
                }
            )
        raise EOFError("Unexpected read")

    mock_transport.read_line = dynamic_read_line  # type: ignore[method-assign]

    token = run_bootstrap_handshake("mock_pipe", 54321, barrier_state)

    assert token == auth_token
    assert barrier_state.is_activated
    assert barrier_state.validate_token(auth_token)
    assert mock_transport.closed
    assert len(mock_transport.client_sent) == 2
    assert mock_transport.client_sent[0]["echoed_challenge"] == challenge
    assert mock_transport.client_sent[0]["port"] == 54321
    assert mock_transport.client_sent[1]["status"] == "active"


def test_handshake_rejects_unsupported_protocol_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify handshake aborts if supervisor sends an unsupported protocol version."""
    barrier_state = AuthBarrierState()
    mock_transport = MockPipeTransport(
        [
            {"protocol_version": 999, "challenge_nonce": "a" * 64},
        ]
    )
    monkeypatch.setattr("postflow.bootstrap.client.get_transport", lambda _p: mock_transport)

    with pytest.raises(ValueError, match="Unsupported bootstrap protocol version"):
        run_bootstrap_handshake("mock_pipe", 54321, barrier_state)

    assert not barrier_state.is_activated
    assert mock_transport.closed


def test_handshake_rejects_invalid_backend_nonce_ack(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify handshake aborts if supervisor responds with an incorrect backend nonce."""
    barrier_state = AuthBarrierState()
    mock_transport = MockPipeTransport(
        [
            {"protocol_version": 1, "challenge_nonce": "a" * 64},
            {
                "auth_token": "b" * 64,
                "backend_nonce_ack": "wrong_nonce_value_00000000000000",
            },
        ]
    )
    monkeypatch.setattr("postflow.bootstrap.client.get_transport", lambda _p: mock_transport)

    with pytest.raises(ValueError, match="Backend nonce mismatch"):
        run_bootstrap_handshake("mock_pipe", 54321, barrier_state)

    assert not barrier_state.is_activated
    assert mock_transport.closed
