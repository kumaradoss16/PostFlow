"""Health verification endpoints for PostFlow development environment.

NOTE: This endpoint is provided strictly for development verification in M1.1.
Production process readiness is handled via the protected bootstrap pipe (M1.2)
and does not rely on an unauthenticated HTTP probe.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from postflow.infrastructure.config import Settings, get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health status response schema."""

    status: str = Field(default="ok", description="Service operational status")
    version: str = Field(..., description="PostFlow backend version")
    environment: str = Field(..., description="Current environment mode")
    host: str = Field(..., description="Listener host (strictly loopback)")


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Development health verification",
)
def get_health(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    """Return basic backend health metadata for development verification."""
    return HealthResponse(
        status="ok",
        version=settings.version,
        environment=settings.environment,
        host=settings.host,
    )
