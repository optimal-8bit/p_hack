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
    SupportedLanguagesResponse,
    DoctorRecommendationInfo
)
from pipeline.orchestrator import get_orchestrator
from pipeline.context_tracker import get_context_tracker
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from models.emotion_fusion import fuse_emotions
from database.db import get_session_history, save_chat_turn, save_crisis_event
from services.doctor_recommendation_service import get_recommendation_service
import config

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponseSchema)
async def chat(request: ChatRequest):
    """Process a chat message with optional facial emotion data"""
    try:
        orchestrator = get_orchestrator()
        
        # Pre-process facial emotion if provided
        override_emotion = None
        override_confidence = None
        facial_emotion_data = None
        
        if request.facial_emotion:
            logger.info(
                f"📹 [EMOTION-FUSION] Received facial emotion data: "
                f"emotion={request.facial_emotion.dominant_emotion}, "
                f"confidence={request.facial_emotion.confidence:.3f}, "
                f"age={request.facial_emotion.age}, "
                f"gender={request.facial_emotion.gender}"
            )
            
            # Store facial emotion data for later use
            facial_emotion_data = {
                "dominant_emotion": request.facial_emotion.dominant_emotion,
                "confidence": request.facial_emotion.confidence,
                "age": request.facial_emotion.age,
                "gender": request.facial_emotion.gender,
                "all_emotions": request.facial_emotion.all_emotions
            }
            
            # Use facial emotion as override (will be fused in orchestrator)
            override_emotion = request.facial_emotion.dominant_emotion
            override_confidence = request.facial_emotion.confidence
        
        # Process message through pipeline with facial emotion override
        response = await orchestrator.process_message(
            session_id=request.session_id,
            user_message=request.message,
            override_emotion=override_emotion,
            override_confidence=override_confidence,
            facial_emotion_data=facial_emotion_data  # Pass full facial data
        )
        
        # If facial emotion was provided, perform fusion for response metadata
        fusion_result = None
        if request.facial_emotion:
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
        
        # Check if doctor recommendation should be generated
        recommendation_service = get_recommendation_service()
        doctor_recommendation = None
        
        # Get full conversation history for analysis
        context = get_context_tracker().get_context(response.session_id)
        
        # Build messages list from context + current message
        messages = []
        emotions = []
        intents = []
        
        # Add historical context
        for turn in context:
            messages.append({"content": turn.user_text})
            emotions.append(turn.emotion)
            intents.append(turn.intent)
        
        # Add current message
        messages.append({"content": request.message})
        emotions.append(response.emotion)
        intents.append(response.intent)
        
        logger.info(
            f"🔍 [DOCTOR-REC] Analyzing conversation: "
            f"turn={response.turn_number}, messages={len(messages)}, "
            f"emotions={emotions[-3:]}, is_crisis={response.is_crisis}"
        )
        
        # Analyze conversation
        recommendation_data = recommendation_service.analyze_conversation(
            session_id=response.session_id,
            messages=messages,
            emotions=emotions,
            intents=intents,
            is_crisis=response.is_crisis
        )
        
        if recommendation_data:
            logger.info(
                f"✅ [DOCTOR-REC] Recommendation generated: "
                f"specialization={recommendation_data.get('recommended_specialization')}, "
                f"urgency={recommendation_data.get('urgency')}, "
                f"symptoms={len(recommendation_data.get('symptoms', []))}"
            )
            
            # Save recommendation to database
            asyncio.create_task(
                recommendation_service.save_recommendation(recommendation_data)
            )
            
            # Include in response if appropriate
            if recommendation_service.should_show_recommendation(
                response.turn_number,
                has_existing_recommendation=False  # TODO: Check database
            ):
                doctor_recommendation = DoctorRecommendationInfo(
                    should_recommend=True,
                    specialization=recommendation_data.get("recommended_specialization"),
                    reason=recommendation_data.get("reason"),
                    urgency=recommendation_data.get("urgency")
                )
                logger.info(
                    f"🏥 [DOCTOR-REC] Showing recommendation to user: "
                    f"{recommendation_data.get('recommended_specialization')} "
                    f"(urgency: {recommendation_data.get('urgency')})"
                )
            else:
                logger.info(
                    f"⏭️ [DOCTOR-REC] Recommendation generated but not shown yet "
                    f"(turn {response.turn_number})"
                )
        else:
            logger.info(
                f"ℹ️ [DOCTOR-REC] No recommendation needed yet "
                f"(turn {response.turn_number}, symptoms below threshold)"
            )
        
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
            session_id=response.session_id,
            doctor_recommendation=doctor_recommendation
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


@router.get("/api/test-recommendation")
async def test_recommendation():
    """Test endpoint to verify doctor recommendation system is working"""
    try:
        from services.doctor_recommendation_service import get_recommendation_service
        
        service = get_recommendation_service()
        
        # Test with anxiety symptoms
        test_messages = [
            {"content": "I've been feeling really anxious lately"},
            {"content": "I can't sleep and I'm worried all the time"}
        ]
        
        recommendation = service.analyze_conversation(
            session_id="test-session",
            messages=test_messages,
            emotions=["anxiety", "fear"],
            intents=["anxiety and panic"],
            is_crisis=False
        )
        
        return {
            "status": "working",
            "recommendation_generated": recommendation is not None,
            "recommendation": recommendation,
            "threshold": service.recommendation_threshold,
            "message": "Doctor recommendation system is operational"
        }
        
    except Exception as e:
        logger.error(f"Error testing recommendation: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": "Doctor recommendation system encountered an error"
        }
