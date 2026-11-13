"""Tests for health and lifecycle verification endpoints."""

import pytest
from fastapi.testclient import TestClient

from postflow.infrastructure.config import Settings
from postflow.main import create_app
from postflow.middleware.auth_barrier import AUTH_HEADER_NAME, AuthBarrierState

TEST_AUTH_TOKEN = "test-secret-barrier-token-12345678"


@pytest.fixture
def test_barrier_state() -> AuthBarrierState:
    """Fixture providing an activated test barrier state."""
    state = AuthBarrierState(initially_active=True, token=TEST_AUTH_TOKEN, allow_dev_health=True)
    return state


@pytest.fixture
def test_client(test_barrier_state: AuthBarrierState) -> TestClient:
    """Fixture providing a configured FastAPI test client with auth headers."""
    settings = Settings(environment="test")
    app = create_app(settings=settings, barrier_state=test_barrier_state)
    return TestClient(
        app,
        base_url="http://127.0.0.1",
        headers={AUTH_HEADER_NAME: TEST_AUTH_TOKEN},
    )


def test_api_v1_health_endpoint(test_client: TestClient) -> None:
    """Verify /api/v1/health returns 200 with valid metadata."""
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "test"
    assert data["host"] == "127.0.0.1"


def test_root_health_endpoint(test_client: TestClient) -> None:
    """Verify root /health endpoint returns 200 with valid metadata in test mode."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_production_root_health_endpoint_not_mounted() -> None:
    """Verify that in production environment, unauthenticated root /health is 404."""
    barrier_state = AuthBarrierState(initially_active=True, token=TEST_AUTH_TOKEN)
    settings = Settings(environment="production")
    app = create_app(settings=settings, barrier_state=barrier_state)
    client = TestClient(
        app,
        base_url="http://127.0.0.1",
        headers={AUTH_HEADER_NAME: TEST_AUTH_TOKEN},
    )
    assert client.get("/health").status_code == 404


def test_production_api_v1_health_requires_auth_barrier() -> None:
    """Verify that in production, /api/v1/health requires bootstrap and valid auth header."""
    settings = Settings(environment="production")

    # 1. Unactivated barrier -> HTTP 503
    unactivated_barrier = AuthBarrierState(initially_active=False)
    app1 = create_app(settings=settings, barrier_state=unactivated_barrier)
    client1 = TestClient(app1, base_url="http://127.0.0.1")
    assert client1.get("/api/v1/health").status_code == 503

    # 2. Activated barrier, missing header -> HTTP 401
    activated_barrier = AuthBarrierState(initially_active=True, token=TEST_AUTH_TOKEN)
    app2 = create_app(settings=settings, barrier_state=activated_barrier)
    client2 = TestClient(app2, base_url="http://127.0.0.1")
    assert client2.get("/api/v1/health").status_code == 401

    # 3. Activated barrier, valid header -> HTTP 200
    client3 = TestClient(
        app2,
        base_url="http://127.0.0.1",
        headers={AUTH_HEADER_NAME: TEST_AUTH_TOKEN},
    )
    res = client3.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_api_v1_shutdown_endpoint(test_client: TestClient) -> None:
    """Verify POST /api/v1/shutdown responds with acknowledgement."""
    response = test_client.post("/api/v1/shutdown")
    assert response.status_code == 200
    assert response.json()["status"] == "shutting_down"


def test_rejects_untrusted_host_header(test_barrier_state: AuthBarrierState) -> None:
    """Verify requests with untrusted Host header are rejected by TrustedHostMiddleware."""
    settings = Settings(environment="development")
    app = create_app(settings=settings, barrier_state=test_barrier_state)
    client = TestClient(
        app,
        base_url="http://127.0.0.1",
        headers={AUTH_HEADER_NAME: TEST_AUTH_TOKEN},
    )
    response = client.get("/health", headers={"Host": "evil.com"})
    assert response.status_code == 400


def test_health_response_contains_no_sensitive_data(test_client: TestClient) -> None:
    """Verify health endpoint does not disclose sensitive information, paths, or secrets."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"status", "version", "environment", "host"}
    sensitive_keys = {"token", "secret", "password", "path", "database", "key", "config", "debug"}
    assert not sensitive_keys.intersection(data.keys())


def test_production_docs_endpoint_disabled() -> None:
    """Verify that in production environment, API documentation endpoints are disabled."""
    barrier_state = AuthBarrierState(initially_active=True, token=TEST_AUTH_TOKEN)
    settings = Settings(environment="production")
    app = create_app(settings=settings, barrier_state=barrier_state)
    client = TestClient(
        app,
        base_url="http://127.0.0.1",
        headers={AUTH_HEADER_NAME: TEST_AUTH_TOKEN},
    )
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404
