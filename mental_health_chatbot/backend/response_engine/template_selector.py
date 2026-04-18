import random
import logging
from typing import List
from response_engine.templates import RESPONSE_TEMPLATES
from pipeline.context_tracker import TurnRecord
from models.translator import get_translation_manager

logger = logging.getLogger(__name__)

# Emotion acknowledgments to prepend to responses
EMOTION_ACKNOWLEDGMENTS = {
    "sadness": ["I can hear that you're going through something really painful. ", "That sounds incredibly hard. "],
    "fear": ["It sounds like you're feeling really scared right now. ", "I can sense a lot of anxiety in what you're sharing. "],
    "anger": ["I can hear how frustrated you are. ", "That sounds really infuriating. "],
    "joy": ["It's so good to hear some positivity! ", "That's wonderful — "],
    "neutral": ["Thank you for sharing that. ", "I hear you. "],
    "surprise": ["That sounds like it came out of nowhere. ", "Wow, that must have been unexpected. "],
    "disgust": ["It sounds like something really bothered you. ", "That sounds deeply uncomfortable. "],
}


class TemplateSelector:
    def __init__(self):
        self.translator = get_translation_manager()
    
    def select(
        self,
        emotion: str,
        intent: str,
        turn_number: int,
        context: List[TurnRecord],
        detected_language: str = "en"
    ) -> str:
        """Select appropriate response template"""
        
        # Determine turn stage
        if turn_number <= 2:
            turn_stage = "opening"
        elif turn_number <= 4:
            turn_stage = "middle"
        else:
            turn_stage = "deeper"
        
        logger.debug(f"Selecting template: emotion={emotion}, intent={intent}, turn_stage={turn_stage}")
        
        # Try to find exact match
        template_variants = self._get_template_variants(emotion, intent, turn_stage)
        
        # If no match, try fallbacks
        if not template_variants:
            logger.debug(f"No exact match, trying fallbacks")
            # Fallback 1: same emotion + general emotional support
            template_variants = self._get_template_variants(emotion, "general emotional support", turn_stage)
        
        if not template_variants:
            # Fallback 2: neutral + general emotional support
            template_variants = self._get_template_variants("neutral", "general emotional support", turn_stage)
        
        if not template_variants:
            # Fallback 3: UNKNOWN
            template_variants = RESPONSE_TEMPLATES.get("UNKNOWN", [
                "Thank you for sharing that with me. I'm listening—can you tell me a little more about what you're going through?"
            ])
        
        # Select variant that hasn't been used recently
        selected_template = self._select_unused_variant(template_variants, context)
        
        # Get emotion acknowledgment
        acknowledgment = self.get_emotion_acknowledgment(emotion)
        
        # Combine acknowledgment + template
        response = acknowledgment + selected_template
        
        # Translate if needed
        if detected_language != "en":
            response = self.translator.translate_from_english(response, detected_language)
        
        return response
    
    def _get_template_variants(self, emotion: str, intent: str, turn_stage: str) -> List[str]:
        """Get template variants for emotion × intent × turn_stage"""
        try:
            return RESPONSE_TEMPLATES[emotion][intent][turn_stage]
        except KeyError:
            return []
    
    def _select_unused_variant(self, variants: List[str], context: List[TurnRecord]) -> str:
        """Select a variant that hasn't been used recently in this session"""
        if not context:
            return random.choice(variants)
        
        # Get recently used template keys (last 3 turns)
        recent_templates = [turn.response_template_key for turn in context[-3:]]
        
        # Filter out recently used variants
        unused_variants = [v for v in variants if v not in recent_templates]
        
        if unused_variants:
            return random.choice(unused_variants)
        else:
            # All have been used, pick randomly
            return random.choice(variants)
    
    def get_emotion_acknowledgment(self, emotion: str) -> str:
        """Get emotion acknowledgment phrase"""
        acknowledgments = EMOTION_ACKNOWLEDGMENTS.get(emotion, ["I hear you. "])
        return random.choice(acknowledgments)


# Singleton instance
_template_selector = None


def get_template_selector() -> TemplateSelector:
    """Get singleton template selector instance"""
    global _template_selector
    if _template_selector is None:
        _template_selector = TemplateSelector()
    return _template_selector
