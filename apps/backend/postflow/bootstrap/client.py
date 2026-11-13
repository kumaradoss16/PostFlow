"""Windows named-pipe bootstrap client for PostFlow backend."""

import json
import secrets
import sys
from typing import Any

from postflow.middleware.auth_barrier import AuthBarrierState

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
    ERROR_FILE_NOT_FOUND = 2
    ERROR_PIPE_BUSY = 231

    _kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

    _kernel32.CreateFileW.restype = wintypes.HANDLE
    _kernel32.CreateFileW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]

    _kernel32.ReadFile.restype = wintypes.BOOL
    _kernel32.ReadFile.argtypes = [
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    ]

    _kernel32.WriteFile.restype = wintypes.BOOL
    _kernel32.WriteFile.argtypes = [
        wintypes.HANDLE,
        wintypes.LPCVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    ]

    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [
        wintypes.HANDLE,
    ]

    _kernel32.WaitNamedPipeW.restype = wintypes.BOOL
    _kernel32.WaitNamedPipeW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
    ]


def is_windows_named_pipe_path(path: str) -> bool:
    """Validate whether the path is a valid Windows named pipe path format.

    Format requirement: \\\\.\\pipe\\<pipename> (case-insensitive)
    The pipe name must be non-empty and must not contain path traversal characters.
    """
    if not isinstance(path, str):
        return False
    normalized = path.strip()
    prefix = "\\\\.\\pipe\\"
    if not normalized.lower().startswith(prefix.lower()):
        return False
    pipe_name = normalized[len(prefix) :]
    if not pipe_name or "/" in pipe_name or "\\" in pipe_name or ".." in pipe_name:
        return False
    return True


class WindowsNamedPipeTransport:
    """Synchronous transport for Windows named pipes using kernel32."""

    def __init__(self, pipe_path: str) -> None:
        self.pipe_path = pipe_path
        self._handle: Any = None
        self._buffer = b""

    def connect(self, timeout_seconds: float = 10.0) -> None:
        """Connect to the parent supervisor named pipe with bounded retry."""
        if sys.platform != "win32":
            raise RuntimeError("WindowsNamedPipeTransport is only supported on Windows.")

        if self._handle is not None:
            return

        import ctypes
        import time

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        deadline = time.monotonic() + timeout_seconds

        while True:
            handle = kernel32.CreateFileW(
                self.pipe_path,
                GENERIC_READ | GENERIC_WRITE,
                0,
                None,
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL,
                None,
            )

            # Check handle validity using 64-bit comparison
            if handle is not None and handle != 0 and handle != INVALID_HANDLE_VALUE:
                self._handle = handle
                return

            err = kernel32.GetLastError()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ConnectionError(
                    f"Timed out after {timeout_seconds}s connecting to supervisor bootstrap pipe "
                    f"'{self.pipe_path}' (last error: {err})"
                )

            # Bounded retry for transient pipe startup states
            if err == ERROR_FILE_NOT_FOUND:
                time.sleep(min(0.05, max(0.001, remaining)))
            elif err == ERROR_PIPE_BUSY:
                wait_ms = max(1, min(int(remaining * 1000), 500))
                kernel32.WaitNamedPipeW(self.pipe_path, wait_ms)
            else:
                # Permanent error
                raise ConnectionError(
                    f"Failed to connect to supervisor bootstrap pipe '{self.pipe_path}', "
                    f"error: {err}"
                )

    def send_line(self, line: str) -> None:
        """Send a newline-terminated UTF-8 line across the pipe."""
        if self._handle is None:
            raise ConnectionError("Named pipe transport is not connected.")

        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        data = line.encode("utf-8")
        if not data.endswith(b"\n"):
            data += b"\n"

        bytes_written = wintypes.DWORD()
        success = kernel32.WriteFile(
            self._handle,
            data,
            len(data),
            ctypes.byref(bytes_written),
            None,
        )
        if not success:
            raise OSError(f"Failed to write to bootstrap pipe, error: {kernel32.GetLastError()}")

    def read_line(self) -> str:
        """Read a single newline-terminated line from the pipe."""
        if self._handle is None:
            raise ConnectionError("Named pipe transport is not connected.")

        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

        while b"\n" not in self._buffer:
            chunk = ctypes.create_string_buffer(4096)
            bytes_read = wintypes.DWORD()
            success = kernel32.ReadFile(
                self._handle,
                chunk,
                4096,
                ctypes.byref(bytes_read),
                None,
            )
            if not success or bytes_read.value == 0:
                raise EOFError("Bootstrap pipe closed by supervisor before complete handshake.")
            self._buffer += chunk.raw[: bytes_read.value]

        line_bytes, _, rest = self._buffer.partition(b"\n")
        self._buffer = rest
        return line_bytes.decode("utf-8").strip()

    def close(self) -> None:
        """Close the pipe handle exactly once and clear buffers."""
        handle = self._handle
        self._handle = None
        self._buffer = b""
        if sys.platform == "win32" and handle is not None:
            if handle != 0 and handle != INVALID_HANDLE_VALUE:
                import ctypes

                ctypes.windll.kernel32.CloseHandle(handle)  # type: ignore[attr-defined]


class SocketOrMockTransport:
    """Fallback transport for testing or non-Windows environments."""

    def __init__(self, target_path: str) -> None:
        self.target_path = target_path
        self._sock = None
        self._file = None

    def connect(self) -> None:
        import socket

        family = getattr(socket, "AF_UNIX", socket.AF_INET)
        self._sock = socket.socket(family, socket.SOCK_STREAM)
        self._sock.connect(self.target_path)
        self._file = self._sock.makefile("rwb", buffering=0)

    def send_line(self, line: str) -> None:
        if not self._file:
            raise ConnectionError("Transport not connected")
        data = line.encode("utf-8")
        if not data.endswith(b"\n"):
            data += b"\n"
        self._file.write(data)
        self._file.flush()

    def read_line(self) -> str:
        if not self._file:
            raise ConnectionError("Transport not connected")
        line = self._file.readline()
        if not line:
            raise EOFError("Connection closed")
        return line.decode("utf-8").strip()

    def close(self) -> None:
        if self._file:
            self._file.close()
        if self._sock:
            self._sock.close()


def get_transport(pipe_path: str) -> Any:
    """Factory selecting the appropriate transport."""
    if sys.platform == "win32" and is_windows_named_pipe_path(pipe_path):
        return WindowsNamedPipeTransport(pipe_path)
    return SocketOrMockTransport(pipe_path)


def run_bootstrap_handshake(
    pipe_path: str,
    bound_port: int,
    barrier_state: AuthBarrierState,
) -> str:
    """Execute the bidirectional challenge-response bootstrap protocol.

    1. Connect to supervisor pipe.
    2. Receive BootstrapInit { protocol_version, challenge_nonce }.
    3. Send BootstrapReady { echoed_challenge, port, backend_nonce }.
    4. Receive BootstrapAuthorize { auth_token, backend_nonce_ack }.
    5. Activate authentication barrier with auth_token.
    6. Send BootstrapAck { status: "active" }.
    7. Close transport and return auth_token.
    """
    transport = get_transport(pipe_path)
    transport.connect()
    try:
        # Step 1: Read BootstrapInit
        init_raw = transport.read_line()
        init_data = json.loads(init_raw)

        protocol_version = init_data.get("protocol_version")
        if protocol_version != 1:
            raise ValueError(f"Unsupported bootstrap protocol version: {protocol_version}")

        challenge_nonce = init_data.get("challenge_nonce")
        if not challenge_nonce or len(challenge_nonce) < 32:
            raise ValueError("Invalid challenge nonce received from supervisor.")

        # Step 2: Generate backend nonce and reply with BootstrapReady
        backend_nonce = secrets.token_hex(32)
        ready_payload = {
            "echoed_challenge": challenge_nonce,
            "port": bound_port,
            "backend_nonce": backend_nonce,
        }
        transport.send_line(json.dumps(ready_payload))

        # Step 3: Receive BootstrapAuthorize
        auth_raw = transport.read_line()
        auth_data = json.loads(auth_raw)

        backend_nonce_ack = auth_data.get("backend_nonce_ack")
        if not backend_nonce_ack or not secrets.compare_digest(backend_nonce_ack, backend_nonce):
            raise ValueError("Backend nonce mismatch in supervisor authorization response.")

        auth_token = auth_data.get("auth_token")
        if not auth_token or len(auth_token) < 32:
            raise ValueError("Invalid authentication token provisioned by supervisor.")

        # Step 4: Activate barrier
        barrier_state.activate(auth_token)

        # Step 5: Send final acknowledgement
        ack_payload = {"status": "active"}
        transport.send_line(json.dumps(ack_payload))

        return auth_token
    finally:
        transport.close()
