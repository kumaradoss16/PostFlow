"""Authentication activation barrier middleware.

Enforces that the backend remains completely inaccessible to application HTTP
requests until the protected bootstrap handshake has authorized activation.
Once activated, every HTTP request must provide a valid X-PostFlow-Local-Auth token.
"""

import secrets
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

AUTH_HEADER_NAME = "X-PostFlow-Local-Auth"


class AuthBarrierState:
    """Manages the lifecycle and authorization state of the local backend."""

    def __init__(
        self,
        initially_active: bool = False,
        token: str | None = None,
        allow_dev_health: bool = False,
    ) -> None:
        self._activated = initially_active
        self._auth_token = token
        self._allow_dev_health = allow_dev_health

    @property
    def is_activated(self) -> bool:
        """Check if authentication barrier has been authorized."""
        return self._activated

    @property
    def allow_dev_health(self) -> bool:
        """Check if unauthenticated /health is permitted for local dev verification."""
        return self._allow_dev_health

    @allow_dev_health.setter
    def allow_dev_health(self, value: bool) -> None:
        self._allow_dev_health = bool(value)

    def activate(self, token: str) -> None:
        """Authorize the barrier and configure the active authentication secret."""
        if not token or len(token) < 16:
            raise ValueError("Authentication token must contain at least 16 characters.")
        self._auth_token = token
        self._activated = True

    def reset(self) -> None:
        """Reset the barrier to unactivated state and clear in-memory credentials."""
        self._auth_token = None
        self._activated = False

    def validate_token(self, provided_token: str | None) -> bool:
        """Validate the provided token using constant-time comparison."""
        if not self._activated or not self._auth_token or not provided_token:
            return False
        return secrets.compare_digest(provided_token.strip(), self._auth_token.strip())


_GLOBAL_BARRIER_STATE = AuthBarrierState()


def get_auth_barrier_state() -> AuthBarrierState:
    """Retrieve global barrier state instance."""
    return _GLOBAL_BARRIER_STATE


class AuthenticationBarrierMiddleware(BaseHTTPMiddleware):
    """ASGI Middleware enforcing the M1.2 authentication activation barrier."""

    def __init__(
        self,
        app: ASGIApp,
        barrier_state: AuthBarrierState | None = None,
    ) -> None:
        super().__init__(app)
        self.barrier_state = barrier_state or _GLOBAL_BARRIER_STATE

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Any],
    ) -> Response:
        # Pre-flight OPTIONS requests for CORS are allowed through
        if request.method == "OPTIONS":
            return await call_next(request)

        # Allow development health probe if explicitly configured for dev/test
        if self.barrier_state.allow_dev_health and request.url.path == "/health":
            return await call_next(request)

        # 1. Gate: Backend must be authorized through the bootstrap protocol
        if not self.barrier_state.is_activated:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "error": "backend_not_ready",
                    "detail": "Bootstrap authentication handshake is incomplete",
                },
            )

        # 2. Gate: Every request must supply valid X-PostFlow-Local-Auth header
        provided_token = request.headers.get(AUTH_HEADER_NAME)
        if not self.barrier_state.validate_token(provided_token):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "unauthorized",
                    "detail": "Missing or invalid local authentication credential",
                },
            )

        return await call_next(request)
