"""Tests for health verification endpoints."""

import pytest
from fastapi.testclient import TestClient

from postflow.infrastructure.config import Settings
from postflow.main import create_app


@pytest.fixture
def test_client() -> TestClient:
    """Fixture providing a configured FastAPI test client."""
    settings = Settings(environment="test")
    app = create_app(settings=settings)
    return TestClient(app, base_url="http://127.0.0.1")


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
    """Verify root /health endpoint returns 200 with valid metadata."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_production_environment_omits_unauthenticated_health_endpoints() -> None:
    """Verify that in production environment, unauthenticated health routes are omitted."""
    settings = Settings(environment="production")
    app = create_app(settings=settings)
    client = TestClient(app, base_url="http://127.0.0.1")
    assert client.get("/health").status_code == 404
    assert client.get("/api/v1/health").status_code == 404


def test_rejects_untrusted_host_header() -> None:
    """Verify requests with untrusted Host header are rejected by TrustedHostMiddleware."""
    settings = Settings(environment="development")
    app = create_app(settings=settings)
    client = TestClient(app, base_url="http://127.0.0.1")
    # Send request with hostile Host header
    response = client.get("/health", headers={"Host": "evil.com"})
    assert response.status_code == 400
