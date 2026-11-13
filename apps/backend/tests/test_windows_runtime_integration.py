"""Real Windows Named Pipe, Child Process Lifecycle, and Graceful Shutdown Integration Test."""

import ctypes
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from ctypes import wintypes

import pytest


@pytest.mark.skipif(
    sys.platform != "win32", reason="Windows named-pipe runtime test requires Windows"
)
def test_real_windows_backend_bootstrap_and_graceful_shutdown() -> None:
    """Execute end-to-end integration test against real Python child process on 64-bit Windows.

    1. Pre-creates real Windows named pipe server (F3 race elimination).
    2. Spawns real child process with --bootstrap-pipe.
    3. Completes challenge/nonce exchange via 64-bit ctypes pipe transport (F1, F2).
    4. Probes authenticated loopback HTTP endpoint.
    5. Coordinates graceful shutdown via POST /api/v1/shutdown (F5).
    6. Confirms child process terminates cleanly with exit code 0 within timeout.
    7. Confirms no orphan process remains.
    """
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

    PIPE_ACCESS_DUPLEX = 0x00000003
    PIPE_TYPE_BYTE = 0x00000000
    PIPE_READMODE_BYTE = 0x00000000
    PIPE_WAIT = 0x00000000
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    kernel32.CreateNamedPipeW.restype = wintypes.HANDLE
    kernel32.CreateNamedPipeW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
    ]

    kernel32.ConnectNamedPipe.restype = wintypes.BOOL
    kernel32.ConnectNamedPipe.argtypes = [wintypes.HANDLE, wintypes.LPVOID]

    kernel32.ReadFile.restype = wintypes.BOOL
    kernel32.ReadFile.argtypes = [
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    ]

    kernel32.WriteFile.restype = wintypes.BOOL
    kernel32.WriteFile.argtypes = [
        wintypes.HANDLE,
        wintypes.LPCVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    ]

    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

    pipe_name = f"\\\\.\\pipe\\postflow-test-{uuid.uuid4()}"

    # Step 1: Pre-create named pipe server (F3)
    server_handle = kernel32.CreateNamedPipeW(
        pipe_name,
        PIPE_ACCESS_DUPLEX,
        PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,
        1,
        4096,
        4096,
        0,
        None,
    )
    assert server_handle != INVALID_HANDLE_VALUE and server_handle != 0

    child = None
    try:
        # Step 2: Spawn real child process running postflow.main
        python_exe = sys.executable
        cmd = [python_exe, "-m", "postflow.main", "--bootstrap-pipe", pipe_name]
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        child = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

        child_pid = child.pid
        assert child_pid > 0

        # Step 3: Await client connection
        connected = kernel32.ConnectNamedPipe(server_handle, None)
        # 0 or False may be returned if client already connected (ERROR_PIPE_CONNECTED = 535)
        if not connected:
            err = kernel32.GetLastError()
            assert err == 535, f"ConnectNamedPipe failed with unexpected error: {err}"

        # Helper functions for pipe I/O
        def send_line(msg: str) -> None:
            data = (msg + "\n").encode("utf-8")
            written = wintypes.DWORD()
            success = kernel32.WriteFile(
                server_handle, data, len(data), ctypes.byref(written), None
            )
            assert success, f"WriteFile failed: {kernel32.GetLastError()}"

        buffer = b""

        def read_line() -> str:
            nonlocal buffer
            while b"\n" not in buffer:
                chunk = ctypes.create_string_buffer(4096)
                read_bytes = wintypes.DWORD()
                success = kernel32.ReadFile(
                    server_handle, chunk, 4096, ctypes.byref(read_bytes), None
                )
                assert success and read_bytes.value > 0, (
                    f"ReadFile failed: {kernel32.GetLastError()}"
                )
                buffer += chunk.raw[: read_bytes.value]
            line, _, rest = buffer.partition(b"\n")
            buffer = rest
            return line.decode("utf-8").strip()

        # Step 4: Execute challenge / nonce handshake
        challenge_nonce = secrets.token_hex(32)
        init_payload = {
            "protocol_version": 1,
            "challenge_nonce": challenge_nonce,
        }
        send_line(json.dumps(init_payload))

        ready_raw = read_line()
        ready_data = json.loads(ready_raw)
        assert ready_data["echoed_challenge"] == challenge_nonce
        backend_port = ready_data["port"]
        assert backend_port > 0
        backend_nonce = ready_data["backend_nonce"]

        auth_token = secrets.token_hex(32)
        auth_payload = {
            "auth_token": auth_token,
            "backend_nonce_ack": backend_nonce,
        }
        send_line(json.dumps(auth_payload))

        ack_raw = read_line()
        ack_data = json.loads(ack_raw)
        assert ack_data["status"] == "active"

        # Step 5: Verify authenticated HTTP endpoint with bounded wait for Uvicorn readiness
        health_url = f"http://127.0.0.1:{backend_port}/api/v1/health"
        req = urllib.request.Request(
            health_url,
            headers={"X-PostFlow-Local-Auth": auth_token, "Host": "127.0.0.1"},
        )
        start_poll = time.monotonic()
        body = None
        while time.monotonic() - start_poll < 10.0:
            try:
                with urllib.request.urlopen(req, timeout=2) as resp:
                    if resp.status == 200:
                        body = json.loads(resp.read().decode("utf-8"))
                        break
            except (urllib.error.URLError, TimeoutError, OSError):
                time.sleep(0.1)

        assert body is not None, "Failed to connect to backend after 10 seconds"
        assert body["status"] == "ok"
        assert body["host"] == "127.0.0.1"

        # Step 6: Verify production root /health is protected and not mounted
        root_health_url = f"http://127.0.0.1:{backend_port}/health"
        # 6a: Unauthenticated request is rejected by AuthenticationBarrierMiddleware with 401
        with pytest.raises(urllib.error.HTTPError) as exc_info_unauth:
            urllib.request.urlopen(
                urllib.request.Request(root_health_url, headers={"Host": "127.0.0.1"}),
                timeout=5,
            )
        assert exc_info_unauth.value.code == 401

        # 6b: Even with valid auth header, root /health is 404 (not mounted in production)
        with pytest.raises(urllib.error.HTTPError) as exc_info_auth:
            urllib.request.urlopen(
                urllib.request.Request(
                    root_health_url,
                    headers={"X-PostFlow-Local-Auth": auth_token, "Host": "127.0.0.1"},
                ),
                timeout=5,
            )
        assert exc_info_auth.value.code == 404

        # Step 7: Trigger graceful shutdown via POST /api/v1/shutdown (F5)
        shutdown_url = f"http://127.0.0.1:{backend_port}/api/v1/shutdown"
        shutdown_req = urllib.request.Request(
            shutdown_url,
            data=b"",
            headers={"X-PostFlow-Local-Auth": auth_token, "Host": "127.0.0.1"},
            method="POST",
        )
        with urllib.request.urlopen(shutdown_req, timeout=5) as resp:
            assert resp.status == 200
            body = json.loads(resp.read().decode("utf-8"))
            assert body["status"] == "shutting_down"

        # Step 8: Confirm child process terminates cleanly within 5 seconds with code 0
        exit_code = child.wait(timeout=5)
        assert exit_code == 0, f"Child exited with non-zero exit code: {exit_code}"
        assert child.poll() == 0

        # Step 9: Verify child process is dead and not still active
        STILL_ACTIVE = 259
        exit_code_dword = wintypes.DWORD()
        child_any: object = child
        child_raw_handle = int(getattr(child_any, "_handle", 0))
        kernel32.GetExitCodeProcess(
            wintypes.HANDLE(child_raw_handle), ctypes.byref(exit_code_dword)
        )
        assert exit_code_dword.value == 0
        assert exit_code_dword.value != STILL_ACTIVE

    finally:
        # Cleanup
        if server_handle != INVALID_HANDLE_VALUE and server_handle != 0:
            kernel32.CloseHandle(server_handle)
        if child and child.poll() is None:
            child.kill()
            child.wait()


@pytest.mark.skipif(
    sys.platform != "win32", reason="Windows named-pipe runtime test requires Windows"
)
def test_real_windows_child_unexpected_termination_and_restart() -> None:
    """Verify detection of unexpected child process exit, endpoint invalidation,
    and successful restart.
    """
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

    PIPE_ACCESS_DUPLEX = 0x00000003
    PIPE_TYPE_BYTE = 0x00000000
    PIPE_READMODE_BYTE = 0x00000000
    PIPE_WAIT = 0x00000000
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    def run_instance() -> tuple[subprocess.Popen[bytes], int, str]:
        pipe_name = f"\\\\.\\pipe\\postflow-test-{uuid.uuid4()}"
        srv_handle = kernel32.CreateNamedPipeW(
            pipe_name,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,
            1,
            4096,
            4096,
            0,
            None,
        )
        assert srv_handle != INVALID_HANDLE_VALUE

        proc = subprocess.Popen(
            [sys.executable, "-m", "postflow.main", "--bootstrap-pipe", pipe_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )

        connected = kernel32.ConnectNamedPipe(srv_handle, None)
        if not connected:
            assert kernel32.GetLastError() == 535

        def send_line(msg: str) -> None:
            data = (msg + "\n").encode("utf-8")
            written = wintypes.DWORD()
            kernel32.WriteFile(srv_handle, data, len(data), ctypes.byref(written), None)

        buffer = b""

        def read_line() -> str:
            nonlocal buffer
            while b"\n" not in buffer:
                chunk = ctypes.create_string_buffer(4096)
                read_bytes = wintypes.DWORD()
                kernel32.ReadFile(srv_handle, chunk, 4096, ctypes.byref(read_bytes), None)
                buffer += chunk.raw[: read_bytes.value]
            line, _, rest = buffer.partition(b"\n")
            buffer = rest
            return line.decode("utf-8").strip()

        challenge = secrets.token_hex(32)
        send_line(json.dumps({"protocol_version": 1, "challenge_nonce": challenge}))
        ready = json.loads(read_line())
        port = ready["port"]
        backend_nonce = ready["backend_nonce"]

        token = secrets.token_hex(32)
        send_line(json.dumps({"auth_token": token, "backend_nonce_ack": backend_nonce}))
        ack = json.loads(read_line())
        assert ack["status"] == "active"
        kernel32.CloseHandle(srv_handle)

        return proc, port, token

    # Instance 1: start, kill unexpectedly, verify termination
    proc1, port1, token1 = run_instance()
    time.sleep(0.3)

    # Health check succeeds while alive
    req = urllib.request.Request(
        f"http://127.0.0.1:{port1}/api/v1/health",
        headers={"X-PostFlow-Local-Auth": token1, "Host": "127.0.0.1"},
    )
    with urllib.request.urlopen(req, timeout=3) as resp:
        assert resp.status == 200

    # Simulate unexpected process crash/kill
    proc1.kill()
    proc1.wait(timeout=3)
    assert proc1.poll() is not None

    # Verify requests to the terminated instance are rejected / connection refused
    with pytest.raises((urllib.error.URLError, ConnectionRefusedError, OSError)):
        urllib.request.urlopen(req, timeout=1)

    # Instance 2: verify restart works cleanly with new pipe and port
    proc2, port2, token2 = run_instance()
    time.sleep(0.3)
    try:
        req2 = urllib.request.Request(
            f"http://127.0.0.1:{port2}/api/v1/health",
            headers={"X-PostFlow-Local-Auth": token2, "Host": "127.0.0.1"},
        )
        with urllib.request.urlopen(req2, timeout=3) as resp:
            assert resp.status == 200
    finally:
        # Graceful shutdown of instance 2
        shutdown_req = urllib.request.Request(
            f"http://127.0.0.1:{port2}/api/v1/shutdown",
            data=b"",
            headers={"X-PostFlow-Local-Auth": token2, "Host": "127.0.0.1"},
            method="POST",
        )
        with urllib.request.urlopen(shutdown_req, timeout=3) as resp:
            assert resp.status == 200
        assert proc2.wait(timeout=5) == 0
