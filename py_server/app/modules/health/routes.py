from fastapi import APIRouter

from app.modules.health.controller import get_health
from app.modules.health.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return await get_health()
