"""
API Routes
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """API health check"""
    return {"status": "ok"}
