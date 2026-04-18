import logging
import time
import asyncio
from dataclasses import dataclass
from typing import Optional

from voice.transcriber import get_transcriber
from voice.audio_analyzer import get_audio_analyzer
from voice.word_attributor import get_word_attributor
from voice.fusion_engine import get_fusion_engine, FusionResult
from pipeline.safety import get_safety_checker
from pipeline.orchestrator import get_orchestrator
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model

logger = logging.getLogger(__name__)


@dataclass
class VoiceChatResponse:
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
    
    word_analysis: list
    stressed_words: list
    
    chat_result: Optional[object]  # ChatResponse from orchestrator


class VoicePipeline:
    def __init__(self):
        self.transcriber = get_transcriber()
        self.audio_analyzer = get_audio_analyzer()
        self.word_attributor = get_word_attributor()
        self.fusion_engine = get_fusion_engine()
        self.safety_checker = get_safety_checker()
        self.orchestrator = get_orchestrator()
        self.emotion_model = get_emotion_model()
        self.intent_model = get_intent_model()
        
        logger.info("Voice pipeline initialized")
    
    async def process_audio(
        self,
        session_id: str,
        audio_path: str
    ) -> VoiceChatResponse:
        """Process audio through the full voice pipeline"""
        try:
            # Step 1: Transcribe audio
            logger.info(f"Transcribing audio for session {session_id}")
            transcription_start = time.time()
            
            transcription_result = await self._run_in_executor(
                self.transcriber.transcribe,
                audio_path
            )
            
            transcription_time = (time.time() - transcription_start) * 1000
            logger.info(f"Transcription complete in {transcription_time:.0f}ms: {transcription_result.text}")
            
            # Step 2: Check if transcript is empty
            if not transcription_result.text.strip():
                logger.warning("Empty transcript received")
                return self._create_error_response(
                    "I couldn't hear anything in the audio. Could you try again?",
                    transcription_result.duration_seconds,
                    transcription_time
                )
            
            # Step 3: Safety check on transcript
            safety_result = await self._run_in_executor(
                self.safety_checker.check,
                transcription_result.text
            )
            
            if safety_result.is_crisis:
                logger.warning(f"Crisis detected in voice message: {safety_result.crisis_type}")
                # Return crisis response with empty word analysis
                crisis_response = self._create_crisis_response(
                    safety_result.response,
                    transcription_result,
                    transcription_time
                )
                logger.info(f"Returning crisis response with message: {crisis_response.chat_result.response_text[:100]}...")
                logger.info(f"Crisis flag set: {crisis_response.chat_result.is_crisis}")
                return crisis_response
            
            # Step 4: Analyze audio features
            logger.info("Analyzing audio features")
            fusion_start = time.time()
            
            # Analyze full clip baseline
            baseline = await self._run_in_executor(
                self.audio_analyzer.analyze_clip,
                audio_path
            )
            logger.info(f"📊 Speaker baseline: pitch={baseline.pitch_mean:.1f}Hz, amplitude={baseline.amplitude_mean:.3f}")
            
            # Analyze each word's audio features
            audio_features = []
            for word_ts in transcription_result.words:
                word_feat = await self._run_in_executor(
                    self.audio_analyzer.analyze_word,
                    audio_path,
                    word_ts.start,
                    word_ts.end,
                    baseline,
                    word_ts.word
                )
                audio_features.append(word_feat)
                logger.debug(f"🎵 Word '{word_feat.word}': pitch={word_feat.pitch_normalized:.2f}, amp={word_feat.amplitude_normalized:.2f}, stressed={word_feat.is_stressed}, hint={word_feat.emotion_hint}")
            
            logger.info(f"✓ Analyzed {len(audio_features)} words from audio")
            
            # Step 5: Compute text weights
            logger.info("Computing text attribution weights")
            text_weights = await self._run_in_executor(
                self.word_attributor.compute_text_weights,
                transcription_result.text,
                transcription_result.words,
                self.emotion_model
            )
            logger.info(f"✓ Computed text weights for {len(text_weights)} words")
            
            # Step 6: Run fusion engine
            logger.info("Running fusion engine")
            fusion_result = await self._run_in_executor(
                self.fusion_engine.fuse,
                transcription_result.text,
                transcription_result.words,
                text_weights,
                audio_features,
                self.emotion_model,
                self.intent_model
            )
            
            fusion_time = (time.time() - fusion_start) * 1000
            logger.info(f"Fusion complete in {fusion_time:.0f}ms")
            logger.info(f"🎯 Text-only emotion: {fusion_result.text_only_emotion} ({fusion_result.text_only_confidence:.2f})")
            logger.info(f"🎵 Audio-focused emotion: {fusion_result.audio_focused_emotion} ({fusion_result.audio_focused_confidence:.2f})")
            logger.info(f"⚡ FUSED emotion: {fusion_result.fused_emotion} ({fusion_result.fused_confidence:.2f})")
            if fusion_result.is_incongruent:
                logger.warning(f"⚠️  INCONGRUENCE DETECTED: {fusion_result.incongruence_note}")
            if fusion_result.stressed_words:
                logger.info(f"💪 Stressed words: {', '.join(fusion_result.stressed_words)}")
            
            # Step 7: Call orchestrator with fused emotion
            logger.info("Calling orchestrator for response generation")
            chat_result = await self.orchestrator.process_message(
                session_id=session_id,
                user_message=transcription_result.text,
                override_emotion=fusion_result.fused_emotion,
                override_confidence=fusion_result.fused_confidence
            )
            
            # Step 8: Build and return response
            return VoiceChatResponse(
                transcript=transcription_result.text,
                detected_language=transcription_result.language,
                audio_duration_seconds=transcription_result.duration_seconds,
                transcription_time_ms=transcription_time,
                fusion_time_ms=fusion_time,
                text_only_emotion=fusion_result.text_only_emotion,
                text_only_confidence=fusion_result.text_only_confidence,
                audio_focused_emotion=fusion_result.audio_focused_emotion,
                audio_focused_confidence=fusion_result.audio_focused_confidence,
                fused_emotion=fusion_result.fused_emotion,
                fused_confidence=fusion_result.fused_confidence,
                intent=fusion_result.intent,
                intent_confidence=fusion_result.intent_confidence,
                is_incongruent=fusion_result.is_incongruent,
                incongruence_score=fusion_result.incongruence_score,
                incongruence_note=fusion_result.incongruence_note,
                word_analysis=[
                    {
                        "word": wr.word,
                        "final_weight": wr.final_weight,
                        "text_weight": wr.text_weight,
                        "audio_weight": wr.audio_weight,
                        "pitch_normalized": wr.pitch_normalized,
                        "amplitude_normalized": wr.amplitude_normalized,
                        "is_stressed": wr.is_stressed,
                        "emotion_hint": wr.emotion_hint
                    }
                    for wr in fusion_result.word_results
                ],
                stressed_words=fusion_result.stressed_words,
                chat_result=chat_result
            )
            
        except Exception as e:
            logger.error(f"Voice pipeline error: {e}", exc_info=True)
            # Return graceful fallback
            return self._create_error_response(
                "I encountered an error processing your audio. Please try again.",
                0.0,
                0.0
            )
    
    async def _run_in_executor(self, func, *args):
        """Run synchronous function in executor to avoid blocking event loop"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args)
    
    def _create_error_response(
        self,
        error_message: str,
        duration: float,
        transcription_time: float
    ) -> VoiceChatResponse:
        """Create error response"""
        return VoiceChatResponse(
            transcript="",
            detected_language="en",
            audio_duration_seconds=duration,
            transcription_time_ms=transcription_time,
            fusion_time_ms=0.0,
            text_only_emotion="neutral",
            text_only_confidence=0.0,
            audio_focused_emotion="neutral",
            audio_focused_confidence=0.0,
            fused_emotion="neutral",
            fused_confidence=0.0,
            intent="general emotional support",
            intent_confidence=0.0,
            is_incongruent=False,
            incongruence_score=0.0,
            incongruence_note="",
            word_analysis=[],
            stressed_words=[],
            chat_result=None
        )
    
    def _create_crisis_response(
        self,
        crisis_message: str,
        transcription_result,
        transcription_time: float
    ) -> VoiceChatResponse:
        """Create crisis response"""
        # Create a mock chat result with crisis response
        # This matches the ChatResponse dataclass from orchestrator
        from dataclasses import dataclass
        
        @dataclass
        class CrisisChatResult:
            response_text: str
            detected_language: str
            emotion: str
            emotion_confidence: float
            intent: str
            intent_confidence: float
            turn_number: int
            is_crisis: bool
            processing_time_ms: float
            session_id: str
        
        crisis_chat_result = CrisisChatResult(
            response_text=crisis_message,
            detected_language=transcription_result.language,
            emotion="fear",
            emotion_confidence=1.0,
            intent="anxiety and panic",
            intent_confidence=1.0,
            turn_number=1,
            is_crisis=True,  # THIS IS THE KEY FLAG
            processing_time_ms=transcription_time,
            session_id="crisis"
        )
        
        logger.info(f"Created crisis chat result with is_crisis={crisis_chat_result.is_crisis}")
        
        return VoiceChatResponse(
            transcript=transcription_result.text,
            detected_language=transcription_result.language,
            audio_duration_seconds=transcription_result.duration_seconds,
            transcription_time_ms=transcription_time,
            fusion_time_ms=0.0,
            text_only_emotion="fear",
            text_only_confidence=1.0,
            audio_focused_emotion="fear",
            audio_focused_confidence=1.0,
            fused_emotion="fear",
            fused_confidence=1.0,
            intent="anxiety and panic",
            intent_confidence=1.0,
            is_incongruent=False,
            incongruence_score=0.0,
            incongruence_note="",
            word_analysis=[],
            stressed_words=[],
            chat_result=crisis_chat_result
        )


# Singleton instance
_voice_pipeline: Optional[VoicePipeline] = None


def get_voice_pipeline() -> VoicePipeline:
    """Get singleton voice pipeline instance"""
    global _voice_pipeline
    if _voice_pipeline is None:
        _voice_pipeline = VoicePipeline()
    return _voice_pipeline
