"""PostFlow backend application entry point and factory."""

import argparse
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from postflow import __version__
from postflow.api.v1 import api_v1_router
from postflow.api.v1.health import router as root_health_router
from postflow.infrastructure.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application instance."""
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title="PostFlow Backend",
        version=__version__,
        description="Local-first desktop backend engine for PostFlow",
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url=None,
    )

    # Wire settings dependency override
    app.dependency_overrides[get_settings] = lambda: settings

    allowed_hosts = ["127.0.0.1", "localhost"]
    if settings.environment == "test":
        allowed_hosts.append("testserver")

    # Restrict host header to loopback
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )

    # Restrict CORS to trusted local origins
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

    # Register API routes
    app.include_router(api_v1_router)
    # Also mount root health router for direct /health queries
    app.include_router(root_health_router, prefix="", tags=["health"])

    return app


def main() -> None:
    """Main CLI execution entry point for local development."""
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

    args = parser.parse_args()

    # Enforce loopback check at CLI boundary
    if args.host.strip() != "127.0.0.1":
        print(
            f"ERROR: Refusing to bind to '{args.host}'. PostFlow backend only binds to 127.0.0.1.",
            file=sys.stderr,
        )
        sys.exit(1)

    import uvicorn

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
        app = create_app()
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=args.port,
            reload=False,
            log_level="info",
        )


if __name__ == "__main__":
    main()
