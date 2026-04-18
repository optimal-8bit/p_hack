from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=1000)


class EmotionScore(BaseModel):
    emotion: str
    confidence: float
    all_scores: Dict[str, float]


class IntentScore(BaseModel):
    intent: str
    confidence: float


class ChatResponseSchema(BaseModel):
    response_text: str
    detected_language: str
    emotion: EmotionScore
    intent: IntentScore
    turn_number: int
    is_crisis: bool
    processing_time_ms: float
    session_id: str


class SessionHistoryItem(BaseModel):
    user_message: str
    bot_response: str
    emotion: str
    intent: str
    timestamp: str


class SessionHistoryResponse(BaseModel):
    session_id: str
    turns: List[SessionHistoryItem]
    total_turns: int


class HealthResponse(BaseModel):
    status: str
    models_loaded: Dict[str, bool]
    version: str = "1.0.0"


class LanguageInfo(BaseModel):
    code: str
    name: str


class SupportedLanguagesResponse(BaseModel):
    languages: List[LanguageInfo]
