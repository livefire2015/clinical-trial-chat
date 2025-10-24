"""
AG-UI Endpoint for Agent Communication via SSE
"""
import json
from typing import AsyncIterator
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse
from pydantic import BaseModel

from app.agent.clinical_agent import get_agent

router = APIRouter()


class Message(BaseModel):
    """AG-UI message format"""
    role: str
    content: str


class RunAgentInput(BaseModel):
    """AG-UI RunAgentInput format"""
    messages: list[Message]


async def event_stream(agent, messages: list[Message]) -> AsyncIterator[str]:
    """
    Stream AG-UI events from agent execution

    Yields SSE-formatted events
    """
    # Convert AG-UI messages to Pydantic AI format
    message_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages[:-1]  # All but last message
    ]

    user_prompt = messages[-1].content if messages else ""

    try:
        # Send start event
        yield f"data: {json.dumps({'type': 'run_start'})}\n\n"

        # Run agent and stream response
        async with agent.run_stream(user_prompt) as result:
            async for chunk in result.stream_text(delta=True):
                # Send message delta events
                event = {
                    "type": "message_delta",
                    "delta": {"content": chunk}
                }
                yield f"data: {json.dumps(event)}\n\n"

            # Get final result
            final_result = await result.get_data()

            # Send completion event
            completion_event = {
                "type": "message_done",
                "message": {
                    "role": "assistant",
                    "content": final_result if isinstance(final_result, str) else str(final_result)
                }
            }
            yield f"data: {json.dumps(completion_event)}\n\n"

    except Exception as e:
        # Send error event
        error_event = {
            "type": "error",
            "error": str(e)
        }
        yield f"data: {json.dumps(error_event)}\n\n"

    # Send done event
    yield f"data: {json.dumps({'type': 'run_done'})}\n\n"


@router.post("/agent/run")
async def run_agent(request: Request) -> StreamingResponse:
    """
    AG-UI endpoint for running the clinical trial analysis agent.

    Accepts RunAgentInput via POST and streams AG-UI events via SSE.
    """
    agent = get_agent()

    # Parse AG-UI request
    body = await request.json()
    run_input = RunAgentInput(**body)

    # Stream AG-UI events
    return StreamingResponse(
        event_stream(agent, run_input.messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
