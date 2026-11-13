"""API v1 route registrations."""

from fastapi import APIRouter

from postflow.api.v1.health import router as health_router
from postflow.api.v1.shutdown import router as shutdown_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health_router, prefix="", tags=["health"])
api_v1_router.include_router(shutdown_router, prefix="", tags=["lifecycle"])

__all__ = ["api_v1_router"]
