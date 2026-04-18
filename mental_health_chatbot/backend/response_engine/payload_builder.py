"""
Structured Payload Builder for LLM Generation
Constructs the structured data payload that controls LLM output
"""

import logging
from typing import Dict, List, Optional
from pipeline.context_tracker import TurnRecord

logger = logging.getLogger(__name__)


class PayloadBuilder:
    """Builds structured payload for controlled LLM generation"""
    
    def build_llm_payload(
        self,
        user_input: str,
        processed_text: str,
        message_type: Dict,
        emotion: str,
        emotion_confidence: float,
        intent: str,
        intent_confidence: float,
        turn_number: int,
        context: List[TurnRecord],
        response_components: Dict,
        allow_therapist: bool = False
    ) -> Dict:
        """
        Build structured payload for LLM generation
        
        Args:
            user_input: Original user message
            processed_text: Cleaned/translated text
            message_type: Message type detection result
            emotion: Detected emotion
            emotion_confidence: Emotion confidence score
            intent: Detected intent
            intent_confidence: Intent confidence score
            turn_number: Current turn number
            context: Conversation context
            response_components: Generated response components
            allow_therapist: Whether therapist suggestion is allowed
            
        Returns:
            Structured payload dict for LLM
        """
        
        # Extract context information
        context_info = self._extract_context_info(context)
        
        # Determine decision engine strategy
        strategy_info = self._determine_strategy(
            message_type, emotion, emotion_confidence, turn_number, context
        )
        
        # Build response plan from components
        response_plan = self._build_response_plan(response_components)
        
        # Construct payload
        payload = {
            "user_input": user_input,
            "processed_text": processed_text,
            "message_type": {
                "type": message_type.get("type", "emotional"),
                "confidence": message_type.get("confidence", 0.5),
                "reason": message_type.get("reason", "")
            },
            "emotion": {
                "label": emotion,
                "confidence": emotion_confidence
            },
            "intent": {
                "label": intent,
                "confidence": intent_confidence
            },
            "context": context_info,
            "decision_engine": strategy_info,
            "response_plan": response_plan,
            "constraints": {
                "max_sentences": 4,
                "style": "empathetic, natural, non-clinical",
                "no_diagnosis": True,
                "no_new_advice": True,
                "strict_plan": True,
                "allow_therapist": allow_therapist
            }
        }
        
        logger.debug(f"Built LLM payload for {message_type.get('type')} message")
        return payload
    
    def _extract_context_info(self, context: List[TurnRecord]) -> Dict:
        """Extract relevant context information"""
        if not context:
            return {
                "turn_number": 1,
                "dominant_emotion": None,
                "previous_emotions": [],
                "recent_messages": [],
                "topics": []
            }
        
        # Get recent emotions (last 3 turns)
        recent_emotions = [turn.emotion for turn in context[-3:]]
        
        # Get dominant emotion
        emotion_counts = {}
        for turn in context:
            emotion_counts[turn.emotion] = emotion_counts.get(turn.emotion, 0) + 1
        dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else None
        
        # Get recent messages (last 2 turns, user text only)
        recent_messages = [turn.user_text for turn in context[-2:]]
        
        # Extract basic topics (simple keyword extraction)
        topics = self._extract_topics(context)
        
        return {
            "turn_number": len(context) + 1,
            "dominant_emotion": dominant_emotion,
            "previous_emotions": recent_emotions,
            "recent_messages": recent_messages,
            "topics": topics
        }
    
    def _extract_topics(self, context: List[TurnRecord]) -> List[str]:
        """Extract mentioned topics from conversation"""
        topics = set()
        
        # Common topic keywords
        topic_keywords = {
            "work": ["work", "job", "career", "office", "boss", "colleague"],
            "school": ["school", "exam", "test", "study", "homework", "class"],
            "family": ["family", "parent", "mother", "father", "sibling", "child"],
            "relationship": ["relationship", "partner", "boyfriend", "girlfriend", "marriage"],
            "health": ["health", "sick", "pain", "doctor", "hospital", "medical"],
            "money": ["money", "financial", "debt", "bills", "income", "budget"]
        }
        
        # Check last 3 messages for topics
        recent_text = " ".join([turn.user_text.lower() for turn in context[-3:]])
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in recent_text for keyword in keywords):
                topics.add(topic)
        
        return list(topics)[:3]  # Limit to 3 topics
    
    def _determine_strategy(
        self,
        message_type: Dict,
        emotion: str,
        emotion_confidence: float,
        turn_number: int,
        context: List[TurnRecord]
    ) -> Dict:
        """Determine decision engine strategy"""
        
        msg_type = message_type.get("type", "emotional")
        
        # Determine tone based on emotion and confidence
        if emotion_confidence < 0.6:
            tone = "gentle, uncertain"
        elif emotion in ["sadness", "fear", "anger"]:
            tone = "empathetic, supportive"
        elif emotion == "joy":
            tone = "warm, encouraging"
        else:
            tone = "neutral, supportive"
        
        # Determine depth based on turn number and message type
        if msg_type == "short_reply":
            depth = "surface"
        elif turn_number <= 2:
            depth = "exploratory"
        elif turn_number <= 4:
            depth = "moderate"
        else:
            depth = "deeper"
        
        # Determine strategy list
        strategy = []
        if msg_type == "emotional":
            strategy = ["validate", "reflect", "explore"]
        elif msg_type == "contextual":
            strategy = ["acknowledge", "continue", "explore"]
        elif msg_type == "short_reply":
            strategy = ["acknowledge", "clarify"]
        else:  # neutral
            strategy = ["gentle_explore", "open_ended"]
        
        return {
            "strategy": strategy,
            "tone": tone,
            "depth": depth,
            "message_type": msg_type
        }
    
    def _build_response_plan(self, components: Dict) -> Dict:
        """Build response plan from components"""
        
        # Extract components (may be None)
        validation = components.get("validation", "")
        reflection = components.get("reflection", "")
        normalization = components.get("normalization", "")
        coping = components.get("coping", "")
        gentle_guidance = components.get("gentle_guidance", "")
        question = components.get("question", "")
        
        # Build structured plan
        plan = {
            "validation": validation if validation else None,
            "reflection": reflection if reflection else None,
            "normalization": normalization if normalization else None,
            "coping": coping if coping else None,
            "gentle_guidance": gentle_guidance if gentle_guidance else None,
            "question": question if question else None
        }
        
        # Remove None values
        plan = {k: v for k, v in plan.items() if v is not None}
        
        return plan


# Singleton instance
_payload_builder: Optional[PayloadBuilder] = None


def get_payload_builder() -> PayloadBuilder:
    """Get singleton payload builder instance"""
    global _payload_builder
    if _payload_builder is None:
        _payload_builder = PayloadBuilder()
    return _payload_builder