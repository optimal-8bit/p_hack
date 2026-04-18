from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class FacialEmotionData(BaseModel):
    """Facial emotion detected from webcam using face-api.js"""
    dominant_emotion: str
    confidence: float
    all_emotions: Dict[str, float] = Field(default_factory=dict)
    age: Optional[int] = None
    gender: Optional[str] = None
    timestamp: Optional[float] = None


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=1000)
    facial_emotion: Optional[FacialEmotionData] = None  # Optional webcam emotion data


class EmotionScore(BaseModel):
    emotion: str
    confidence: float
    all_scores: Dict[str, float]
    facial_emotion: Optional[str] = None  # Emotion from webcam
    facial_confidence: Optional[float] = None
    is_multimodal: bool = False  # True if both text and facial emotions were used
    emotion_congruence: Optional[str] = None  # "congruent", "incongruent", or None


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
    doctor_recommendation: Optional[DoctorRecommendationInfo] = None


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


class DoctorRecommendationInfo(BaseModel):
    """Doctor recommendation info to include in chat response"""
    should_recommend: bool
    specialization: Optional[str] = None
    reason: Optional[str] = None
    urgency: Optional[str] = None


# Voice pipeline schemas
class FusedWordResultSchema(BaseModel):
    word: str
    final_weight: float
    text_weight: float
    audio_weight: float
    pitch_normalized: float
    amplitude_normalized: float
    is_stressed: bool
    emotion_hint: str


class VoiceChatResponseSchema(BaseModel):
    transcript: str
    detected_language: str
    audio_duration_seconds: float
    transcription_time_ms: float
    fusion_time_ms: float
    
    text_only_emotion: str
    text_only_confidence: float
    audio_focused_emotion: str
    audio_focused_confidence: float
    fused_emotion: str
    fused_confidence: float
    
    intent: str
    intent_confidence: float
    
    is_incongruent: bool
    incongruence_score: float
    incongruence_note: str
    
    word_analysis: List[FusedWordResultSchema]
    stressed_words: List[str]
    
    chat_result: Optional[ChatResponseSchema]  # nest full existing chat response here
