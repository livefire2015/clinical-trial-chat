"""
AG-UI Endpoint for Agent Communication via SSE
"""
from typing import AsyncIterator
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse
from pydantic_ai.ag_ui import handle_ag_ui_request

from app.agent.clinical_agent import get_agent

router = APIRouter()


@router.post("/agent/run")
async def run_agent(request: Request) -> StreamingResponse:
    """
    AG-UI endpoint for running the clinical trial analysis agent.

    Accepts RunAgentInput via POST and streams AG-UI events via SSE.
    """
    agent = get_agent()

    # Use Pydantic-AI's AG-UI integration to handle request and stream events
    return await handle_ag_ui_request(agent, request)
