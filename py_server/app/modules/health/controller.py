"""
Health controller for handling diagnosis requests.
"""
from typing import List, Optional

from app.modules.health.schemas import (
    HealthResponse,
    DiagnosisResponse,
    DiagnosisHistoryResponse
)
from app.modules.health.service import health_status, analyze_patient, get_history


async def get_health() -> HealthResponse:
    """Get system health status."""
    result = await health_status()
    return HealthResponse(**result)


async def diagnose_patient(
    symptoms: List[str],
    image_base64: Optional[str] = None
) -> DiagnosisResponse:
    """
    Diagnose patient based on symptoms and optional image.
    
    Args:
        symptoms: List of symptom names
        image_base64: Optional base64-encoded image
        
    Returns:
        Diagnosis response
    """
    result = await analyze_patient(symptoms, image_base64)
    return DiagnosisResponse(**result)


async def get_diagnosis_history(limit: int = 10) -> DiagnosisHistoryResponse:
    """
    Get diagnosis history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        Diagnosis history response
    """
    result = await get_history(limit)
    return DiagnosisHistoryResponse(**result)
