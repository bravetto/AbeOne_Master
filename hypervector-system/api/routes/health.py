"""
Health Check Routes

Health and status endpoints.
"""

from fastapi import APIRouter
from ..models import HealthResponse

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status and version
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )

