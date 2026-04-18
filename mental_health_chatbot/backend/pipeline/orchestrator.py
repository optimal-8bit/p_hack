import logging
import time
import asyncio
from dataclasses import dataclass
from typing import Optional

from pipeline.safety import get_safety_checker
from pipeline.preprocessor import get_preprocessor
from pipeline.context_tracker import get_context_tracker, TurnRecord
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from response_engine.template_selector import get_template_selector

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
        self.emotion_model = get_emotion_model()
        self.intent_model = get_intent_model()
        self.template_selector = get_template_selector()
        
        logger.info("Chat orchestrator initialized")
    
    async def process_message(self, session_id: str, user_message: str) -> ChatResponse:
        """Process user message through the full pipeline"""
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
            
            # Step 2: Preprocess (clean, detect language, translate)
            preprocessed = await self._run_in_executor(
                self.preprocessor.preprocess, user_message
            )
            logger.debug(f"Preprocessed: lang={preprocessed.language}, translated={preprocessed.was_translated}")
            
            # Step 3: Emotion classification
            emotion_result = await self._run_in_executor(
                self.emotion_model.predict, preprocessed.english_text
            )
            logger.debug(f"Emotion: {emotion_result['emotion']} ({emotion_result['confidence']:.2f})")
            
            # Step 4: Intent classification
            intent_result = await self._run_in_executor(
                self.intent_model.predict, preprocessed.english_text
            )
            logger.debug(f"Intent: {intent_result['intent']} ({intent_result['confidence']:.2f})")
            
            # Step 5: Get context
            turn_number = self.context_tracker.get_turn_number(session_id)
            context = self.context_tracker.get_context(session_id)
            
            # Step 6: Select response
            response_text = await self._run_in_executor(
                self.template_selector.select,
                emotion_result['emotion'],
                intent_result['intent'],
                turn_number,
                context,
                preprocessed.language
            )
            
            # Step 7: Save turn to context
            turn_record = TurnRecord(
                user_text=preprocessed.cleaned,
                emotion=emotion_result['emotion'],
                intent=intent_result['intent'],
                response_template_key=response_text[:50],  # Use first 50 chars as key
                turn_number=turn_number,
                timestamp=time.time()
            )
            self.context_tracker.add_turn(session_id, turn_record)
            
            # Step 8: Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            logger.info(f"Processed message in {processing_time:.0f}ms")
            
            # Step 9: Save to database (async, non-blocking)
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
            
            # Step 10: Return response
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
