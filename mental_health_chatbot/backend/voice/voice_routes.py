import logging
import tempfile
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from voice.voice_pipeline import get_voice_pipeline
from voice.transcriber import get_transcriber
from api.schemas import VoiceChatResponseSchema, FusedWordResultSchema, ChatResponseSchema, EmotionScore, IntentScore

logger = logging.getLogger(__name__)

voice_router = APIRouter()

# Supported audio formats
SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a", ".webm", ".ogg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@voice_router.post("/api/voice/chat", response_model=VoiceChatResponseSchema)
async def voice_chat(
    session_id: str = Form(...),
    audio: UploadFile = File(...)
):
    """Process voice message with audio-fused emotion detection"""
    temp_path = None
    
    try:
        # Validate file extension
        file_ext = os.path.splitext(audio.filename)[1].lower()
        if file_ext not in SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Supported: {', '.join(SUPPORTED_FORMATS)}"
            )
        
        # Read file content
        content = await audio.read()
        
        # Validate file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.0f}MB"
            )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_path = temp_file.name
            temp_file.write(content)
        
        logger.info(f"Processing voice message for session {session_id}, file: {audio.filename}")
        
        # Process through voice pipeline
        voice_pipeline = get_voice_pipeline()
        result = await voice_pipeline.process_audio(session_id, temp_path)
        
        # Convert chat_result to schema if present
        chat_result_schema = None
        if result.chat_result:
            chat_result_schema = ChatResponseSchema(
                response_text=result.chat_result.response_text,
                detected_language=result.chat_result.detected_language,
                emotion=EmotionScore(
                    emotion=result.chat_result.emotion,
                    confidence=result.chat_result.emotion_confidence,
                    all_scores={}
                ),
                intent=IntentScore(
                    intent=result.chat_result.intent,
                    confidence=result.chat_result.intent_confidence
                ),
                turn_number=result.chat_result.turn_number,
                is_crisis=result.chat_result.is_crisis,
                processing_time_ms=result.chat_result.processing_time_ms,
                session_id=result.chat_result.session_id
            )
        
        # Build response schema
        return VoiceChatResponseSchema(
            transcript=result.transcript,
            detected_language=result.detected_language,
            audio_duration_seconds=result.audio_duration_seconds,
            transcription_time_ms=result.transcription_time_ms,
            fusion_time_ms=result.fusion_time_ms,
            text_only_emotion=result.text_only_emotion,
            text_only_confidence=result.text_only_confidence,
            audio_focused_emotion=result.audio_focused_emotion,
            audio_focused_confidence=result.audio_focused_confidence,
            fused_emotion=result.fused_emotion,
            fused_confidence=result.fused_confidence,
            intent=result.intent,
            intent_confidence=result.intent_confidence,
            is_incongruent=result.is_incongruent,
            incongruence_score=result.incongruence_score,
            incongruence_note=result.incongruence_note,
            word_analysis=[
                FusedWordResultSchema(**word) for word in result.word_analysis
            ],
            stressed_words=result.stressed_words,
            chat_result=chat_result_schema
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in voice chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process voice message")
    
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                logger.debug(f"Cleaned up temp file: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_path}: {e}")


@voice_router.get("/api/voice/health")
async def voice_health():
    """Check voice pipeline health"""
    try:
        transcriber = get_transcriber()
        
        # Check if librosa is available
        librosa_available = False
        try:
            import librosa
            librosa_available = True
        except ImportError:
            pass
        
        # Check if ffmpeg is available
        ffmpeg_available = False
        try:
            import subprocess
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                timeout=5
            )
            ffmpeg_available = result.returncode == 0
        except Exception:
            pass
        
        return {
            "whisper_loaded": transcriber.is_loaded(),
            "whisper_model": "small" if transcriber.is_loaded() else None,
            "librosa_available": librosa_available,
            "ffmpeg_available": ffmpeg_available,
            "supported_formats": list(SUPPORTED_FORMATS),
            "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024)
        }
        
    except Exception as e:
        logger.error(f"Error in voice health check: {e}", exc_info=True)
        return {
            "whisper_loaded": False,
            "whisper_model": None,
            "librosa_available": False,
            "ffmpeg_available": False,
            "supported_formats": list(SUPPORTED_FORMATS),
            "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024)
        }
