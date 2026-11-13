"""Graceful shutdown endpoint for PostFlow local backend."""

import os
import signal
import sys

from fastapi import APIRouter, BackgroundTasks, Request, status
from pydantic import BaseModel, Field

router = APIRouter()


class ShutdownResponse(BaseModel):
    """Shutdown acknowledgement response."""

    status: str = Field(default="shutting_down", description="Shutdown status indication")


@router.post(
    "/shutdown",
    response_model=ShutdownResponse,
    status_code=status.HTTP_200_OK,
    summary="Trigger graceful backend shutdown",
)
async def shutdown(request: Request, background_tasks: BackgroundTasks) -> ShutdownResponse:
    """Initiate graceful server shutdown sequence.

    Sets server.should_exit on the running Uvicorn server after the response
    has been dispatched, allowing active requests to drain and FastAPI lifespan
    cleanup handlers to execute cleanly.
    """
    server = getattr(request.app.state, "server", None)

    def _trigger_exit() -> None:
        if server is not None:
            server.should_exit = True
        else:
            if sys.platform != "win32":
                os.kill(os.getpid(), signal.SIGINT)

    # Background task executes immediately after the response is sent to caller
    background_tasks.add_task(_trigger_exit)

    return ShutdownResponse(status="shutting_down")
