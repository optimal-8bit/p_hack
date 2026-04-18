"""
Health routes for diagnosis API.
"""
from fastapi import APIRouter, Query

from app.modules.health.controller import (
    get_health,
    diagnose_patient,
    get_diagnosis_history
)
from app.modules.health.schemas import (
    HealthResponse,
    DiagnosisRequest,
    DiagnosisResponse,
    DiagnosisHistoryResponse
)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check system health status."""
    return await get_health()


@router.post("/analyze", response_model=DiagnosisResponse)
async def analyze_diagnosis(request: DiagnosisRequest) -> DiagnosisResponse:
    """
    Analyze patient symptoms and image to provide diagnosis.
    
    This endpoint performs offline AI-based diagnosis using:
    - Image analysis (if image provided)
    - Symptom analysis
    - Combined decision engine
    
    Works completely offline without external API calls.
    """
    return await diagnose_patient(
        symptoms=request.symptoms,
        image_base64=request.image_base64
    )


@router.get("/history", response_model=DiagnosisHistoryResponse)
async def get_history(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records")
) -> DiagnosisHistoryResponse:
    """
    Get diagnosis history from local database.
    """
    return await get_diagnosis_history(limit)
