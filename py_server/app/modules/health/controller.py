from app.modules.health.schemas import HealthResponse
from app.modules.health.service import health_status


async def get_health() -> HealthResponse:
    result = await health_status()
    return HealthResponse(**result)
