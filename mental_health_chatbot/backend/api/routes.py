import logging
import asyncio
from fastapi import APIRouter, HTTPException
from api.schemas import (
    ChatRequest,
    ChatResponseSchema,
    EmotionScore,
    IntentScore,
    SessionHistoryResponse,
    SessionHistoryItem,
    HealthResponse,
    LanguageInfo,
    SupportedLanguagesResponse
)
from pipeline.orchestrator import get_orchestrator
from pipeline.context_tracker import get_context_tracker
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from models.emotion_fusion import fuse_emotions
from database.db import get_session_history, save_chat_turn, save_crisis_event
import config

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponseSchema)
async def chat(request: ChatRequest):
    """Process a chat message with optional facial emotion data"""
    try:
        orchestrator = get_orchestrator()
        
        # Process message through pipeline
        response = await orchestrator.process_message(
            session_id=request.session_id,
            user_message=request.message
        )
        
        # If facial emotion data is provided, fuse it with text emotion
        fusion_result = None
        if request.facial_emotion:
            logger.info(
                f"📹 [EMOTION-FUSION] Received facial emotion data: "
                f"emotion={request.facial_emotion.dominant_emotion}, "
                f"confidence={request.facial_emotion.confidence:.3f}, "
                f"age={request.facial_emotion.age}, "
                f"gender={request.facial_emotion.gender}"
            )
            
            fusion_result = fuse_emotions(
                text_emotion=response.emotion,
                text_confidence=response.emotion_confidence,
                facial_emotion=request.facial_emotion.dominant_emotion,
                facial_confidence=request.facial_emotion.confidence,
                facial_all_scores=request.facial_emotion.all_emotions
            )
            
            logger.info(
                f"🧠 [EMOTION-FUSION] Fusion completed: "
                f"text_emotion={response.emotion}({response.emotion_confidence:.3f}), "
                f"facial_emotion={request.facial_emotion.dominant_emotion}({request.facial_emotion.confidence:.3f}), "
                f"fused_emotion={fusion_result['fused_emotion']}({fusion_result['fused_confidence']:.3f}), "
                f"congruence={fusion_result.get('congruence')}"
            )
            
            # Update response with fused emotion
            response.emotion = fusion_result["fused_emotion"]
            response.emotion_confidence = fusion_result["fused_confidence"]
            
            # Log incongruence if detected
            if fusion_result.get("congruence") == "incongruent":
                logger.warning(
                    f"⚠️ [EMOTION-FUSION] INCONGRUENCE DETECTED: {fusion_result['fusion_note']}"
                )
        else:
            logger.info("💬 [EMOTION-FUSION] Text-only emotion analysis (no facial data)")
        
        # Save to database (non-blocking)
        asyncio.create_task(
            save_chat_turn(
                session_id=response.session_id,
                user_message=request.message,
                bot_response=response.response_text,
                emotion=response.emotion,
                intent=response.intent,
                is_crisis=response.is_crisis,
                language=response.detected_language,
                processing_time=response.processing_time_ms
            )
        )
        
        # Save crisis event if applicable
        if response.is_crisis:
            asyncio.create_task(
                save_crisis_event(
                    session_id=response.session_id,
                    crisis_type="crisis_detected"
                )
            )
        
        # Convert to schema
        emotion_score = EmotionScore(
            emotion=response.emotion,
            confidence=response.emotion_confidence,
            all_scores={},
            is_multimodal=fusion_result["is_multimodal"] if fusion_result else False,
            emotion_congruence=fusion_result.get("congruence") if fusion_result else None
        )
        
        # Add facial emotion data if available
        if fusion_result and fusion_result["is_multimodal"]:
            emotion_score.facial_emotion = fusion_result["facial_emotion"]
            emotion_score.facial_confidence = fusion_result["facial_confidence"]
        
        return ChatResponseSchema(
            response_text=response.response_text,
            detected_language=response.detected_language,
            emotion=emotion_score,
            intent=IntentScore(
                intent=response.intent,
                confidence=response.intent_confidence
            ),
            turn_number=response.turn_number,
            is_crisis=response.is_crisis,
            processing_time_ms=response.processing_time_ms,
            session_id=response.session_id
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/session/{session_id}/history", response_model=SessionHistoryResponse)
async def get_history(session_id: str):
    """Get conversation history for a session"""
    try:
        history = await get_session_history(session_id)
        
        return SessionHistoryResponse(
            session_id=session_id,
            turns=[
                SessionHistoryItem(
                    user_message=turn["user_message"],
                    bot_response=turn["bot_response"],
                    emotion=turn["emotion"],
                    intent=turn["intent"],
                    timestamp=turn["timestamp"]
                )
                for turn in history
            ],
            total_turns=len(history)
        )
        
    except Exception as e:
        logger.error(f"Error getting session history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve history")


@router.delete("/api/session/{session_id}")
async def clear_session(session_id: str):
    """Clear in-memory context for a session"""
    try:
        context_tracker = get_context_tracker()
        context_tracker.clear_session(session_id)
        
        return {"status": "cleared", "session_id": session_id}
        
    except Exception as e:
        logger.error(f"Error clearing session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to clear session")


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint - shows status of all models"""
    try:
        emotion_model = get_emotion_model()
        intent_model = get_intent_model()
        
        models_loaded = {
            "emotion_classifier": emotion_model.is_loaded(),
            "intent_classifier": intent_model.is_loaded(),
        }
        
        # Translation models use transformers (not ONNX), so we just note they're available
        for lang_code in config.SUPPORTED_LANGUAGES:
            if lang_code != "en":
                models_loaded[f"translator_{lang_code}"] = True  # Always available via transformers
        
        # Check voice pipeline
        try:
            from voice.transcriber import get_transcriber
            transcriber = get_transcriber()
            models_loaded["voice_pipeline_loaded"] = transcriber.is_loaded()
        except Exception as e:
            logger.warning(f"Voice pipeline check failed: {e}")
            models_loaded["voice_pipeline_loaded"] = False
        
        # Determine overall status
        critical_models = ["emotion_classifier", "intent_classifier"]
        all_critical_loaded = all(models_loaded.get(m, False) for m in critical_models)
        
        status = "healthy" if all_critical_loaded else "degraded"
        
        return HealthResponse(
            status=status,
            models_loaded=models_loaded,
            version="1.0.0"
        )
        
    except Exception as e:
        logger.error(f"Error in health check: {e}", exc_info=True)
        return HealthResponse(
            status="unhealthy",
            models_loaded={},
            version="1.0.0"
        )


@router.get("/api/supported-languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """Get list of supported languages"""
    language_names = {
        "en": "English",
        "hi": "Hindi",
        "fr": "French",
        "es": "Spanish"
    }
    
    return SupportedLanguagesResponse(
        languages=[
            LanguageInfo(code=code, name=language_names.get(code, code))
            for code in config.SUPPORTED_LANGUAGES
        ]
    )
