"""Tests for authentication activation barrier and middleware."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from postflow.middleware.auth_barrier import (
    AUTH_HEADER_NAME,
    AuthBarrierState,
    AuthenticationBarrierMiddleware,
)


@pytest.fixture
def barrier_state() -> AuthBarrierState:
    """Fixture providing a fresh unactivated barrier state."""
    return AuthBarrierState(initially_active=False)


@pytest.fixture
def app_with_barrier(barrier_state: AuthBarrierState) -> FastAPI:
    """Fixture providing a test FastAPI app with barrier middleware and CORS."""
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()
    app.add_middleware(AuthenticationBarrierMiddleware, barrier_state=barrier_state)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/v1/protected")
    def protected_route() -> dict[str, str]:
        return {"data": "confidential"}

    return app


def test_barrier_state_lifecycle(barrier_state: AuthBarrierState) -> None:
    """Verify barrier state transitions, token requirements, and validation."""
    assert not barrier_state.is_activated
    assert not barrier_state.validate_token("any-token")

    with pytest.raises(ValueError, match="at least 16 characters"):
        barrier_state.activate("too-short")

    token = "a" * 32
    barrier_state.activate(token)
    assert barrier_state.is_activated
    assert barrier_state.validate_token(token)
    assert not barrier_state.validate_token("wrong-token-value-0000000000000000")
    assert not barrier_state.validate_token(None)

    barrier_state.reset()
    assert not barrier_state.is_activated
    assert not barrier_state.validate_token(token)


def test_middleware_rejects_unactivated_requests(app_with_barrier: FastAPI) -> None:
    """Verify that requests prior to handshake activation return HTTP 503."""
    client = TestClient(app_with_barrier)
    response = client.get("/api/v1/protected")
    assert response.status_code == 503
    data = response.json()
    assert data["error"] == "backend_not_ready"
    assert "incomplete" in data["detail"]


def test_middleware_rejects_missing_or_invalid_auth_header(
    app_with_barrier: FastAPI,
    barrier_state: AuthBarrierState,
) -> None:
    """Verify that requests with missing or invalid token return HTTP 401."""
    token = "secret-valid-token-32-characters-123"
    barrier_state.activate(token)

    client = TestClient(app_with_barrier)

    # Missing header
    res_missing = client.get("/api/v1/protected")
    assert res_missing.status_code == 401
    assert res_missing.json()["error"] == "unauthorized"

    # Invalid header
    res_invalid = client.get(
        "/api/v1/protected",
        headers={AUTH_HEADER_NAME: "wrong-token-value-12345678901234"},
    )
    assert res_invalid.status_code == 401
    assert res_invalid.json()["error"] == "unauthorized"


def test_middleware_allows_valid_authenticated_requests(
    app_with_barrier: FastAPI,
    barrier_state: AuthBarrierState,
) -> None:
    """Verify that requests with valid auth token are authorized."""
    token = "secret-valid-token-32-characters-123"
    barrier_state.activate(token)

    client = TestClient(app_with_barrier)
    response = client.get(
        "/api/v1/protected",
        headers={AUTH_HEADER_NAME: token},
    )
    assert response.status_code == 200
    assert response.json() == {"data": "confidential"}


def test_middleware_allows_options_preflight(app_with_barrier: FastAPI) -> None:
    """Verify that OPTIONS requests pass through for CORS preflight."""
    client = TestClient(app_with_barrier)
    response = client.options(
        "/api/v1/protected",
        headers={
            "Origin": "http://127.0.0.1:1420",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
