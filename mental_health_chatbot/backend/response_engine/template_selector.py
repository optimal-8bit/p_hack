import random
import logging
from typing import List
from response_engine.templates import RESPONSE_TEMPLATES
from response_engine.advanced_response_builder import get_advanced_response_builder
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
        self.advanced_response_builder = get_advanced_response_builder()
        self.component_usage = {}  # Track component usage per session
    
    def select(
        self,
        emotion: str,
        intent: str,
        turn_number: int,
        context: List[TurnRecord],
        detected_language: str = "en",
        user_text: str = "",
        session_id: str = "default",
        emotion_confidence: float = 1.0,
        message_type_result: dict = None
    ) -> str:
        """Select and enhance response template with advanced intelligence layer"""
        
        # Handle non-emotional message types
        if message_type_result:
            msg_type = message_type_result.get('type', 'emotional')
            
            if msg_type == 'short_reply':
                # For short replies, acknowledge and ask clarifying question
                response = self._generate_short_reply_response(user_text, context, emotion)
                if detected_language != "en":
                    response = self.translator.translate_from_english(response, detected_language)
                return response
            
            elif msg_type == 'contextual':
                # For contextual messages, acknowledge and continue conversation
                response = self._generate_contextual_response(user_text, context, emotion)
                if detected_language != "en":
                    response = self.translator.translate_from_english(response, detected_language)
                return response
            
            elif msg_type == 'neutral':
                # For neutral messages, use gentle exploration
                response = self._generate_neutral_response(user_text, context)
                if detected_language != "en":
                    response = self.translator.translate_from_english(response, detected_language)
                return response
        
        # For emotional messages, use advanced response builder
        # Extract context emotions for advanced builder
        context_emotions = [turn.emotion for turn in context[-5:]] if context else []
        
        # Use advanced response builder directly (bypasses old template system)
        enhanced_response = self.advanced_response_builder.build_response(
            user_text=user_text,
            emotion=emotion,
            emotion_confidence=emotion_confidence,
            intent=intent,
            turn_number=turn_number,
            session_id=session_id,
            context_emotions=context_emotions,
            base_template=""  # Not used in advanced builder
        )
        
        # Translate if needed
        if detected_language != "en":
            enhanced_response = self.translator.translate_from_english(enhanced_response, detected_language)
        
        return enhanced_response
    
    def _should_escalate_support(self, context: List[TurnRecord], current_emotion: str) -> bool:
        """Check if support level should be escalated based on persistent negative emotion"""
        if len(context) < 3:
            return False
        
        # Check last 3 emotions
        recent_emotions = [turn.emotion for turn in context[-3:]]
        
        # Negative emotions that warrant escalation
        negative_emotions = ["sadness", "fear", "anger", "disgust"]
        
        # If current emotion is negative and last 3 were also negative
        if current_emotion in negative_emotions:
            negative_count = sum(1 for e in recent_emotions if e in negative_emotions)
            return negative_count >= 2
        
        return False
    
    def _get_template_variants(self, emotion: str, intent: str, turn_stage: str) -> List[str]:
        """Get template variants for emotion × intent × turn_stage"""
        try:
            return RESPONSE_TEMPLATES[emotion][intent][turn_stage]
        except KeyError:
            return []
    
    def _select_unused_variant(
        self,
        variants: List[str],
        context: List[TurnRecord],
        session_id: str,
        emotion: str,
        intent: str
    ) -> str:
        """Select a variant avoiding both text AND structural repetition"""
        if not context:
            return random.choice(variants)
        
        # Track component usage (structural repetition avoidance)
        component_key = f"{session_id}_{emotion}_{intent}"
        if component_key not in self.component_usage:
            self.component_usage[component_key] = []
        
        # Get recently used template keys (text repetition avoidance)
        recent_templates = [turn.response_template_key for turn in context[-3:]]
        
        # Filter out recently used variants
        unused_variants = [v for v in variants if v[:50] not in recent_templates]
        
        if unused_variants:
            selected = random.choice(unused_variants)
        else:
            # All have been used, pick randomly
            selected = random.choice(variants)
        
        # Track component usage
        self.component_usage[component_key].append(selected[:50])
        self.component_usage[component_key] = self.component_usage[component_key][-5:]
        
        return selected
    
    def get_emotion_acknowledgment(self, emotion: str) -> str:
        """Get emotion acknowledgment phrase (DEPRECATED - now handled by response_builder)"""
        # This method is kept for backward compatibility but is no longer used
        # Response builder handles validation/acknowledgment with variation
        return ""
    
    def _generate_short_reply_response(self, user_text: str, context: List[TurnRecord], emotion: str) -> str:
        """Generate response for short replies (yes, no, ok, etc.)"""
        import random
        
        acknowledgments = [
            "Got it, thank you for sharing that.",
            "I understand.",
            "Thank you for letting me know.",
            "I hear you.",
            "Okay, I appreciate you telling me that."
        ]
        
        follow_ups = [
            "Can you tell me more about what's been on your mind?",
            "What's been the hardest part about this?",
            "How has this been affecting you?",
            "What would help you feel better right now?",
            "Can you share more about how you're feeling?"
        ]
        
        # If there's context, make it more specific
        if context and len(context) > 0:
            last_turn = context[-1]
            if last_turn.emotion in ["sadness", "fear", "anger"]:
                follow_ups = [
                    "It sounds like this has been affecting you recently. What was happening around that time?",
                    "Thank you for sharing. Can you tell me more about what's been going on?",
                    "I appreciate you opening up. What's been the most difficult part?",
                    "That helps me understand. How long have you been feeling this way?",
                    "Thank you. What do you think might help with this?"
                ]
        
        return f"{random.choice(acknowledgments)} {random.choice(follow_ups)}"
    
    def _generate_contextual_response(self, user_text: str, context: List[TurnRecord], emotion: str) -> str:
        """Generate response for contextual follow-ups"""
        import random
        
        acknowledgments = [
            "I see.",
            "That makes sense.",
            "I understand.",
            "Thank you for clarifying.",
            "That's helpful to know."
        ]
        
        continuations = [
            "It sounds like this has been affecting you for a while.",
            "That must have been difficult to deal with.",
            "I can imagine how that would feel.",
            "That sounds really challenging.",
            "It makes sense that you'd feel that way."
        ]
        
        follow_ups = [
            "What was that experience like for you?",
            "How did that make you feel?",
            "What's been the hardest part about it?",
            "How are you coping with this?",
            "What do you think would help?"
        ]
        
        return f"{random.choice(acknowledgments)} {random.choice(continuations)} {random.choice(follow_ups)}"
    
    def _generate_neutral_response(self, user_text: str, context: List[TurnRecord]) -> str:
        """Generate response for neutral messages"""
        import random
        
        gentle_explorations = [
            "I'm here to listen. Is there something on your mind you'd like to talk about?",
            "Thank you for sharing. How have you been feeling lately?",
            "I'm here for you. What's been going on in your life recently?",
            "I appreciate you reaching out. Is there something specific that's been bothering you?",
            "I'm listening. What would be most helpful to talk about right now?",
            "Thank you for being here. What's been on your mind?",
            "I'm here to support you. How can I help you today?"
        ]
        
        return random.choice(gentle_explorations)


# Singleton instance
_template_selector = None


def get_template_selector() -> TemplateSelector:
    """Get singleton template selector instance"""
    global _template_selector
    if _template_selector is None:
        _template_selector = TemplateSelector()
    return _template_selector
