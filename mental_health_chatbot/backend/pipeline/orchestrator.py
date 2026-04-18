import logging
import time
import asyncio
from dataclasses import dataclass
from typing import Optional, Dict

from pipeline.safety import get_safety_checker
from pipeline.preprocessor import get_preprocessor
from pipeline.context_tracker import get_context_tracker, TurnRecord
from pipeline.message_type import get_message_type_detector
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from response_engine.template_selector import get_template_selector
from response_engine.payload_builder import get_payload_builder
from response_engine.gemini_generator import generate_gemini_response

logger = logging.getLogger(__name__)

FALLBACK_RESPONSE = "I'm here to listen. Something went wrong on my end, but I'm still here. Can you share more about how you're feeling?"


@dataclass
class ChatResponse:
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


class ChatOrchestrator:
    def __init__(self):
        self.safety_checker = get_safety_checker()
        self.preprocessor = get_preprocessor()
        self.context_tracker = get_context_tracker()
        self.message_type_detector = get_message_type_detector()
        self.emotion_model = get_emotion_model()
        self.intent_model = get_intent_model()
        self.template_selector = get_template_selector()
        self.payload_builder = get_payload_builder()
        
        logger.info("Chat orchestrator initialized")
    
    async def process_message(
        self,
        session_id: str,
        user_message: str,
        override_emotion: Optional[str] = None,
        override_confidence: Optional[float] = None,
        facial_emotion_data: Optional[Dict] = None
    ) -> ChatResponse:
        """Process user message through the full pipeline
        
        Args:
            session_id: Session identifier
            user_message: User's message text
            override_emotion: Optional emotion to use instead of classification (for multimodal input)
            override_confidence: Optional confidence to use with override_emotion
            facial_emotion_data: Optional facial emotion data (video/image analysis)
        """
        start_time = time.time()
        
        try:
            # Step 1: Safety check (ALWAYS FIRST, on raw text)
            logger.info(f"Processing message for session {session_id}")
            safety_result = await self._run_in_executor(
                self.safety_checker.check, user_message
            )
            
            if safety_result.is_crisis:
                # Immediate crisis response, skip all other processing
                processing_time = (time.time() - start_time) * 1000
                logger.warning(f"Crisis detected for session {session_id}: {safety_result.crisis_type}")
                
                # Save crisis event
                from database.db import save_crisis_event, save_chat_turn
                asyncio.create_task(
                    save_crisis_event(session_id, safety_result.crisis_type)
                )
                asyncio.create_task(
                    save_chat_turn(
                        session_id=session_id,
                        user_message=user_message,
                        bot_response=safety_result.response,
                        emotion="fear",
                        intent="anxiety and panic",
                        is_crisis=True,
                        language="en",
                        processing_time=processing_time
                    )
                )
                
                return ChatResponse(
                    response_text=safety_result.response,
                    detected_language="en",  # Crisis response is always in English
                    emotion="fear",  # Assume fear for crisis
                    emotion_confidence=1.0,
                    intent="anxiety and panic",
                    intent_confidence=1.0,
                    turn_number=self.context_tracker.get_turn_number(session_id),
                    is_crisis=True,
                    processing_time_ms=processing_time,
                    session_id=session_id
                )
            
            # Step 2: Detect message type (before preprocessing)
            context_available = len(self.context_tracker.get_context(session_id)) > 0
            message_type_result = self.message_type_detector.detect_message_type(
                user_message, context_available
            )
            logger.info(f"Message type: {message_type_result['type']} (confidence: {message_type_result['confidence']:.2f}) - {message_type_result['reason']}")
            
            # Step 3: Preprocess (clean, detect language, translate)
            # For short replies, use previous language to avoid random switching
            if message_type_result['type'] == 'short_reply' and context_available:
                previous_language = self.context_tracker.get_last_language(session_id)
                logger.debug(f"Short reply detected, using previous language: {previous_language}")
            
            preprocessed = await self._run_in_executor(
                self.preprocessor.preprocess, user_message
            )
            logger.debug(f"Preprocessed: lang={preprocessed.language}, translated={preprocessed.was_translated}")
            
            # Step 4: Conditional emotion classification based on message type
            # Check if emotion is overridden (from voice pipeline)
            if override_emotion is not None:
                emotion_result = {
                    'emotion': override_emotion,
                    'confidence': override_confidence if override_confidence is not None else 0.8
                }
                logger.info(f"Using override emotion: {override_emotion} ({emotion_result['confidence']:.2f})")
            else:
                skip_emotion_classification = self.message_type_detector.should_skip_emotion_classification(message_type_result)
                
                if skip_emotion_classification:
                    # Use fallback emotion from context
                    context_emotion = self.context_tracker.get_dominant_emotion(session_id)
                    fallback_emotion = self.message_type_detector.get_fallback_emotion(
                        message_type_result, context_emotion
                    )
                    emotion_result = {
                        'emotion': fallback_emotion,
                        'confidence': 0.5  # Low confidence for fallback
                    }
                    logger.info(f"Skipped emotion classification, using fallback: {fallback_emotion}")
                else:
                    # Run normal emotion classification
                    emotion_result = await self._run_in_executor(
                        self.emotion_model.predict, preprocessed.english_text
                    )
                    logger.debug(f"Emotion: {emotion_result['emotion']} ({emotion_result['confidence']:.2f})")
            
            # Step 5: Conditional intent classification based on message type
            if message_type_result['type'] == 'contextual' and context_available:
                # Use previous intent for contextual follow-ups
                previous_intent = self.context_tracker.get_last_intent(session_id)
                intent_result = {
                    'intent': previous_intent if previous_intent else 'general emotional support',
                    'confidence': 0.6  # Moderate confidence for context-based
                }
                logger.info(f"Contextual message, using previous intent: {intent_result['intent']}")
            elif message_type_result['type'] == 'short_reply':
                # Use general emotional support for short replies
                intent_result = {
                    'intent': 'general emotional support',
                    'confidence': 0.5
                }
                logger.info(f"Short reply, using general emotional support")
            else:
                # Run normal intent classification
                intent_result = await self._run_in_executor(
                    self.intent_model.predict, preprocessed.english_text
                )
                logger.debug(f"Intent: {intent_result['intent']} ({intent_result['confidence']:.2f})")
            
            # Step 6: Get context
            turn_number = self.context_tracker.get_turn_number(session_id)
            context = self.context_tracker.get_context(session_id)
            
            # Step 7: Generate response with LLM integration
            try:
                # First get response components from template selector
                response_components = await self._run_in_executor(
                    self.template_selector.select,
                    emotion_result['emotion'],
                    intent_result['intent'],
                    turn_number,
                    context,
                    preprocessed.language,
                    user_message,  # Pass original user text for reflection
                    session_id,  # Pass session ID for personalization
                    emotion_result['confidence'],  # Pass emotion confidence for advanced processing
                    message_type_result,  # Pass message type for appropriate response
                    True  # return_components=True for LLM integration
                )
                
                # Build structured payload for LLM
                llm_payload = self.payload_builder.build_llm_payload(
                    user_input=user_message,
                    processed_text=preprocessed.english_text,
                    message_type=message_type_result,
                    emotion=emotion_result['emotion'],
                    emotion_confidence=emotion_result['confidence'],
                    intent=intent_result['intent'],
                    intent_confidence=intent_result['confidence'],
                    turn_number=turn_number,
                    context=context,
                    response_components=response_components,
                    allow_therapist=response_components.get('allow_therapist', False),
                    facial_emotion_data=facial_emotion_data  # Pass facial emotion data
                )
                
                # Try Gemini generation with fallback
                gemini_response = await generate_gemini_response(llm_payload)
                
                if gemini_response:
                    # Use Gemini-generated response
                    response_text = gemini_response
                    logger.info("Using Gemini-generated response")
                else:
                    # Fallback to template response
                    response_text = response_components.get('assembled_response', 
                                                          "I'm here to listen. Can you share more about how you're feeling?")
                    logger.info("Using template fallback response")
                
                # Translate if needed
                if preprocessed.language != "en":
                    response_text = await self._run_in_executor(
                        self.template_selector.translator.translate_from_english,
                        response_text,
                        preprocessed.language
                    )
                
            except Exception as e:
                logger.error(f"Error in Gemini generation pipeline: {e}")
                # Complete fallback to original template system
                response_text = await self._run_in_executor(
                    self.template_selector.select,
                    emotion_result['emotion'],
                    intent_result['intent'],
                    turn_number,
                    context,
                    preprocessed.language,
                    user_message,
                    session_id,
                    emotion_result['confidence'],
                    message_type_result,
                    False  # return_components=False for fallback
                )
            
            # Step 8: Save turn to context
            turn_record = TurnRecord(
                user_text=preprocessed.cleaned,
                emotion=emotion_result['emotion'],
                intent=intent_result['intent'],
                response_template_key=response_text[:50],  # Use first 50 chars as key
                turn_number=turn_number,
                timestamp=time.time(),
                language=preprocessed.language  # Store language for next turn
            )
            self.context_tracker.add_turn(session_id, turn_record)
            
            # Step 9: Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            logger.info(f"Processed message in {processing_time:.0f}ms")
            
            # Step 10: Save to database (async, non-blocking)
            from database.db import save_chat_turn
            asyncio.create_task(
                save_chat_turn(
                    session_id=session_id,
                    user_message=user_message,
                    bot_response=response_text,
                    emotion=emotion_result['emotion'],
                    intent=intent_result['intent'],
                    is_crisis=False,
                    language=preprocessed.language,
                    processing_time=processing_time
                )
            )
            
            # Step 11: Return response
            return ChatResponse(
                response_text=response_text,
                detected_language=preprocessed.language,
                emotion=emotion_result['emotion'],
                emotion_confidence=emotion_result['confidence'],
                intent=intent_result['intent'],
                intent_confidence=intent_result['confidence'],
                turn_number=turn_number,
                is_crisis=False,
                processing_time_ms=processing_time,
                session_id=session_id
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            processing_time = (time.time() - start_time) * 1000
            
            # Return graceful fallback
            return ChatResponse(
                response_text=FALLBACK_RESPONSE,
                detected_language="en",
                emotion="neutral",
                emotion_confidence=0.0,
                intent="general emotional support",
                intent_confidence=0.0,
                turn_number=self.context_tracker.get_turn_number(session_id),
                is_crisis=False,
                processing_time_ms=processing_time,
                session_id=session_id
            )
    
    async def _run_in_executor(self, func, *args):
        """Run synchronous function in executor to avoid blocking event loop"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args)


# Singleton instance
_orchestrator: Optional[ChatOrchestrator] = None


def get_orchestrator() -> ChatOrchestrator:
    """Get singleton orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ChatOrchestrator()
    return _orchestrator
