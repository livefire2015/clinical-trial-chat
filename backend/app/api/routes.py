"""
API Routes
"""
from fastapi import APIRouter
from .ag_ui import router as ag_ui_router

router = APIRouter()


@router.get("/health")
async def health_check():
    """API health check"""
    return {"status": "ok"}


# Include AG-UI routes
router.include_router(ag_ui_router, tags=["agent"])
