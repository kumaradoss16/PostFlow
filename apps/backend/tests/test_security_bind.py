"""Security negative tests: verify non-loopback host binding fails closed."""

import pytest
from pydantic import ValidationError

from postflow.infrastructure.config import Settings


def test_rejects_wildcard_host_bind() -> None:
    """Verify configuring host='0.0.0.0' raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(host="0.0.0.0")
    assert "Security violation" in str(exc_info.value)
    assert "127.0.0.1" in str(exc_info.value)


def test_rejects_lan_host_bind() -> None:
    """Verify configuring host='192.168.1.100' raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(host="192.168.1.100")
    assert "Security violation" in str(exc_info.value)


def test_rejects_hostname_bind() -> None:
    """Verify configuring host='localhost' instead of numeric 127.0.0.1 raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(host="localhost")
    assert "Security violation" in str(exc_info.value)


def test_accepts_strict_loopback() -> None:
    """Verify configuring exact numeric 127.0.0.1 succeeds."""
    settings = Settings(host="127.0.0.1")
    assert settings.host == "127.0.0.1"
