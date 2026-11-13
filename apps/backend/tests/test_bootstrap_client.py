"""Tests for backend bootstrap handshake client."""

import json
import secrets

import pytest

from postflow.bootstrap.client import run_bootstrap_handshake
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


def test_handshake_successful(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify standard bootstrap handshake succeeds and activates barrier."""
    barrier_state = AuthBarrierState(initially_active=False)
    challenge = secrets.token_hex(32)
    auth_token = secrets.token_hex(32)

    # Simulation: supervisor sends Init, expects Ready, sends Authorize, expects Ack
    mock_transport = MockPipeTransport([])

    def mock_get_transport(_path: str) -> MockPipeTransport:
        return mock_transport

    monkeypatch.setattr("postflow.bootstrap.client.get_transport", mock_get_transport)

    # Configure mock responses dynamically
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
            # Retrieve backend_nonce from client's Ready payload
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
