"""Graceful shutdown endpoint for PostFlow local backend."""

import asyncio
import os
import signal
import sys

from fastapi import APIRouter, status
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
async def shutdown() -> ShutdownResponse:
    """Initiate graceful server shutdown sequence."""

    def _trigger_exit() -> None:
        if sys.platform == "win32":
            # On Windows, send SIGTERM or SIGINT
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            os.kill(os.getpid(), signal.SIGINT)

    # Schedule exit after response is dispatched to caller
    loop = asyncio.get_running_loop()
    loop.call_later(0.1, _trigger_exit)

    return ShutdownResponse(status="shutting_down")
