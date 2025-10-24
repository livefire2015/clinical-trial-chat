"""
AG-UI Endpoint for Agent Communication via SSE
"""
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from pydantic_ai.ag_ui import handle_ag_ui_request

from app.agent.clinical_agent import get_agent

router = APIRouter()


@router.post("/agent/run")
async def run_agent(request: Request) -> Response:
    """
    AG-UI endpoint for running the clinical trial analysis agent.

    Uses Pydantic AI's official AG-UI integration to handle requests
    and stream AG-UI events via SSE.

    Accepts RunAgentInput via POST and streams AG-UI events.
    """
    agent = get_agent()
    return await handle_ag_ui_request(agent, request)
