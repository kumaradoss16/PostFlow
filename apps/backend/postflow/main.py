"""PostFlow backend application entry point and factory."""

import argparse
import socket
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from postflow import __version__
from postflow.api.v1 import api_v1_router
from postflow.api.v1.health import router as root_health_router
from postflow.bootstrap import run_bootstrap_handshake
from postflow.infrastructure.config import Settings, get_settings
from postflow.middleware.auth_barrier import (
    AuthBarrierState,
    AuthenticationBarrierMiddleware,
    get_auth_barrier_state,
)


def create_app(
    settings: Settings | None = None,
    barrier_state: AuthBarrierState | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application instance."""
    if settings is None:
        settings = get_settings()

    if barrier_state is None:
        barrier_state = get_auth_barrier_state()

    # Configure dev health probe allowance
    if settings.environment in ("development", "test"):
        barrier_state.allow_dev_health = True
    else:
        barrier_state.allow_dev_health = False

    app = FastAPI(
        title="PostFlow Backend",
        version=__version__,
        description="Local-first desktop backend engine for PostFlow",
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.environment == "development" else None,
    )

    # Wire settings dependency override
    app.dependency_overrides[get_settings] = lambda: settings

    allowed_hosts = ["127.0.0.1", "localhost"]
    if settings.environment == "test":
        allowed_hosts.append("testserver")

    # 1. Enforce authentication barrier across all endpoints
    app.add_middleware(
        AuthenticationBarrierMiddleware,
        barrier_state=barrier_state,
    )

    # 2. Restrict host header to loopback
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )

    # 3. Restrict CORS to trusted local origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:1420",
            "http://localhost:1420",
            "tauri://localhost",
            "https://tauri.localhost",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # 4. Mount application API routes
    app.include_router(api_v1_router)

    # Root /health is mounted strictly in development and test environments
    if settings.environment in ("development", "test"):
        app.include_router(root_health_router, prefix="", tags=["health"])

    return app


def main() -> None:
    """Main CLI execution entry point for PostFlow backend."""
    parser = argparse.ArgumentParser(description="PostFlow Local Backend")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Listener host address (must be 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind (default: 8000 for dev verification)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )
    parser.add_argument(
        "--bootstrap-pipe",
        type=str,
        default=None,
        help="Named pipe path for supervisor bootstrap authentication",
    )

    args = parser.parse_args()

    # Enforce loopback check at CLI boundary
    if args.host.strip() != "127.0.0.1":
        print(
            f"ERROR: Refusing to bind to '{args.host}'. PostFlow backend only binds to 127.0.0.1.",
            file=sys.stderr,
        )
        sys.exit(1)

    import uvicorn

    barrier_state = get_auth_barrier_state()

    # M1.2 Supervised bootstrap execution mode
    if args.bootstrap_pipe:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        sock.listen(128)
        bound_port = sock.getsockname()[1]

        settings = Settings(port=bound_port, environment="production")
        app = create_app(settings=settings, barrier_state=barrier_state)

        # Run handshake over protected pipe
        run_bootstrap_handshake(args.bootstrap_pipe, bound_port, barrier_state)

        config = uvicorn.Config(app, log_level="info")
        server = uvicorn.Server(config)
        server.run(sockets=[sock])
        return

    # Standalone development mode
    settings = Settings(port=args.port, environment="development")
    barrier_state.activate("dev-insecure-local-bootstrap-token-test")
    barrier_state.allow_dev_health = True
    app = create_app(settings=settings, barrier_state=barrier_state)

    if args.reload:
        uvicorn.run(
            "postflow.main:create_app",
            factory=True,
            host="127.0.0.1",
            port=args.port,
            reload=True,
            log_level="info",
        )
    else:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=args.port,
            reload=False,
            log_level="info",
        )


if __name__ == "__main__":
    main()
