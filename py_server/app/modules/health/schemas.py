from typing import List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    mongo: str


class DiagnosisRequest(BaseModel):
    """Request schema for diagnosis analysis."""
    symptoms: List[str] = Field(
        default_factory=list,
        description="List of symptoms (itching, redness, fever, cough, fatigue)"
    )
    image_base64: Optional[str] = Field(
        None,
        description="Base64-encoded image data (optional)"
    )


class DiagnosisResponse(BaseModel):
    """Response schema for diagnosis analysis."""
    disease: str = Field(..., description="Predicted disease name")
    confidence: float = Field(..., description="Confidence score (0-1)")
    risk_level: str = Field(..., description="Risk level: High, Medium, or Low")
    explanation: str = Field(..., description="Human-readable explanation")
    all_scores: dict = Field(..., description="All disease probabilities")


class DiagnosisHistoryItem(BaseModel):
    """Schema for diagnosis history item."""
    id: int
    symptoms: str
    prediction: str
    confidence: float
    risk_level: str
    explanation: str
    image_path: Optional[str]
    timestamp: str


class DiagnosisHistoryResponse(BaseModel):
    """Response schema for diagnosis history."""
    history: List[DiagnosisHistoryItem]
    count: int
