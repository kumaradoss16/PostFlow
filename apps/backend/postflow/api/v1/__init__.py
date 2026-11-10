"""API v1 route registrations."""

from fastapi import APIRouter

from postflow.api.v1.health import router as health_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health_router, prefix="", tags=["health"])

__all__ = ["api_v1_router"]
