"""Windows named-pipe bootstrap client for PostFlow backend."""

import json
import secrets
import sys
from typing import Any

from postflow.middleware.auth_barrier import AuthBarrierState


class WindowsNamedPipeTransport:
    """Synchronous transport for Windows named pipes using kernel32."""

    def __init__(self, pipe_path: str) -> None:
        self.pipe_path = pipe_path
        self._handle: int | None = None
        self._buffer = b""

    def connect(self) -> None:
        """Connect to the parent supervisor named pipe."""
        if sys.platform != "win32":
            raise RuntimeError("WindowsNamedPipeTransport is only supported on Windows.")

        import ctypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        generic_read = 0x80000000
        generic_write = 0x40000000
        open_existing = 3
        invalid_handle_value = -1

        handle = kernel32.CreateFileW(
            self.pipe_path,
            generic_read | generic_write,
            0,
            None,
            open_existing,
            0,
            None,
        )
        if handle == invalid_handle_value or handle == 0:
            error_code = kernel32.GetLastError()
            raise ConnectionError(
                f"Failed to connect to supervisor bootstrap pipe '{self.pipe_path}', "
                f"error: {error_code}"
            )
        self._handle = handle

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
        """Close the pipe handle and clear buffers."""
        if self._handle is not None and sys.platform == "win32":
            import ctypes

            ctypes.windll.kernel32.CloseHandle(self._handle)  # type: ignore[attr-defined]
            self._handle = None
        self._buffer = b""


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
    if sys.platform == "win32" and pipe_path.startswith(r"\\.\pipe\\"):
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
