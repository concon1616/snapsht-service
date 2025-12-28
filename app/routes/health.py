from datetime import datetime
from fastapi import APIRouter

from ..services.browser_pool import browser_pool
from ..models.schemas import HealthResponse

router = APIRouter(tags=["health"])

_start_time = datetime.utcnow()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Get service health status."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        uptime=(datetime.utcnow() - _start_time).total_seconds(),
        browser=browser_pool.status,
    )


@router.get("/health/ready")
async def readiness_check():
    """Check if service is ready to accept requests."""
    status = browser_pool.status

    if status["initialized"] and status["available_drivers"] > 0:
        return {"ready": True}

    return {"ready": False, "reason": "Browser pool not ready"}
