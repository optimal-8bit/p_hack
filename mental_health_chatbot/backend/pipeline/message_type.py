"""
Message Type Detection - Prevents emotion hallucination on non-emotional inputs
Classifies messages to determine appropriate processing pipeline
"""

import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class MessageTypeDetector:
    """Detects message type to prevent inappropriate emotion classification"""
    
    # Emotional keywords that indicate genuine emotional content
    EMOTIONAL_KEYWORDS = [
        # Negative emotions
        "sad", "depressed", "anxious", "worried", "scared", "afraid", "angry", "mad",
        "frustrated", "upset", "hurt", "pain", "suffering", "hopeless", "helpless",
        "worthless", "alone", "lonely", "isolated", "overwhelmed", "stressed",
        "tired", "exhausted", "broken", "crying", "tears", "hate", "fear",
        # Positive emotions
        "happy", "joy", "excited", "grateful", "thankful", "better", "good",
        "great", "wonderful", "amazing", "love", "peaceful", "calm", "relieved",
        # Emotional expressions
        "feel", "feeling", "felt", "emotion", "mood"
    ]
    
    # Contextual/temporal keywords
    CONTEXTUAL_KEYWORDS = [
        # Time references
        "yesterday", "today", "tomorrow", "ago", "earlier", "later", "before",
        "after", "since", "when", "while", "during", "now", "then", "recently",
        "days", "weeks", "months", "years", "morning", "evening", "night",
        # Contextual
        "because", "so", "but", "however", "although", "though", "if", "when",
        "where", "who", "what", "why", "how", "about", "regarding", "concerning",
        # Question words
        "explain", "tell", "describe", "clarify"
    ]
    
    # Short affirmative/negative replies
    SHORT_REPLIES = [
        "yes", "no", "yeah", "nah", "yep", "nope", "ok", "okay", "sure",
        "maybe", "perhaps", "possibly", "definitely", "absolutely", "exactly",
        "right", "correct", "true", "false", "agree", "disagree", "got it"
    ]
    
    # Neutral conversational phrases
    NEUTRAL_PHRASES = [
        "i see", "i understand", "makes sense", "i guess",
        "i think", "i suppose", "not sure", "don't know", "can't say"
    ]
    
    def detect_message_type(self, text: str, context_available: bool = False) -> Dict[str, any]:
        """
        Detect message type to determine processing approach
        
        Args:
            text: User message
            context_available: Whether conversation context exists
        
        Returns:
            Dict with:
                - type: "emotional", "contextual", "short_reply", "neutral"
                - confidence: 0.0 to 1.0
                - reason: Explanation for classification
        """
        text_lower = text.lower().strip()
        word_count = len(text.split())
        
        # Rule 1: Very short replies (1-3 words)
        if word_count <= 3:
            # Check if it's a short affirmative/negative
            if any(reply in text_lower for reply in self.SHORT_REPLIES):
                return {
                    "type": "short_reply",
                    "confidence": 1.0,
                    "reason": f"Short affirmative/negative reply ({word_count} words)"
                }
            
            # Check for neutral conversational phrases first (before temporal check)
            if any(phrase in text_lower for phrase in self.NEUTRAL_PHRASES):
                return {
                    "type": "neutral",
                    "confidence": 0.9,
                    "reason": f"Neutral conversational phrase ({word_count} words)"
                }
            
            # Check for temporal/contextual keywords
            temporal_words = ["day", "week", "month", "year", "hour", "yesterday", "today", "tomorrow", "just"]
            if (re.search(r'\d+', text) or 
                any(word in text_lower for word in temporal_words) or
                any(word in text_lower for word in self.CONTEXTUAL_KEYWORDS)):
                return {
                    "type": "contextual",
                    "confidence": 0.9,
                    "reason": f"Short temporal/contextual reference ({word_count} words)"
                }
            
            # Check for questions (often contextual)
            if "?" in text:
                return {
                    "type": "contextual",
                    "confidence": 0.8,
                    "reason": f"Short question ({word_count} words)"
                }
            
            # Check if it contains emotional keywords despite being short
            if any(keyword in text_lower for keyword in self.EMOTIONAL_KEYWORDS):
                return {
                    "type": "emotional",
                    "confidence": 0.8,
                    "reason": f"Short but contains emotional keywords ({word_count} words)"
                }
            
            # Default for very short inputs
            return {
                "type": "short_reply",
                "confidence": 0.9,
                "reason": f"Very short input ({word_count} words)"
            }
        
        # Rule 2: Check for strong emotional content
        emotional_keyword_count = sum(1 for keyword in self.EMOTIONAL_KEYWORDS if keyword in text_lower)
        if emotional_keyword_count >= 2:
            return {
                "type": "emotional",
                "confidence": 1.0,
                "reason": f"Multiple emotional keywords ({emotional_keyword_count} found)"
            }
        elif emotional_keyword_count == 1:
            # Single emotional keyword - check context
            if word_count >= 5:
                return {
                    "type": "emotional",
                    "confidence": 0.8,
                    "reason": "Contains emotional keyword with sufficient context"
                }
        
        # Rule 3: Check for contextual/temporal content
        contextual_keyword_count = sum(1 for keyword in self.CONTEXTUAL_KEYWORDS if keyword in text_lower)
        if contextual_keyword_count >= 1:  # Lowered threshold
            # Check if it's asking for explanation/clarification
            if any(word in text_lower for word in ["explain", "tell", "describe", "clarify", "mean"]):
                return {
                    "type": "contextual",
                    "confidence": 0.8,
                    "reason": f"Request for explanation/clarification"
                }
            elif contextual_keyword_count >= 2 or context_available:
                return {
                    "type": "contextual",
                    "confidence": 0.9,
                    "reason": f"Multiple contextual keywords ({contextual_keyword_count} found)"
                }
        
        # Rule 4: Check for neutral conversational phrases (prioritize over contextual)
        if any(phrase in text_lower for phrase in self.NEUTRAL_PHRASES):
            return {
                "type": "neutral",
                "confidence": 0.8,
                "reason": "Neutral conversational phrase"
            }
        
        # Rule 4b: Check for uncertainty expressions (should be neutral, not contextual)
        uncertainty_phrases = ["not sure", "don't know", "can't say", "i'm not sure"]
        if any(phrase in text_lower for phrase in uncertainty_phrases):
            return {
                "type": "neutral",
                "confidence": 0.8,
                "reason": "Uncertainty expression"
            }
        
        # Rule 5: Check for questions (often contextual)
        if "?" in text and word_count <= 8:
            return {
                "type": "contextual",
                "confidence": 0.7,
                "reason": "Short question"
            }
        
        # Rule 6: Default classification based on length and context
        if word_count <= 5 and context_available:
            return {
                "type": "contextual",
                "confidence": 0.6,
                "reason": f"Short input with context available ({word_count} words)"
            }
        
        # Rule 7: If no strong signals, classify as neutral
        if emotional_keyword_count == 0:
            return {
                "type": "neutral",
                "confidence": 0.7,
                "reason": "No emotional keywords detected"
            }
        
        # Default: Treat as emotional (conservative approach)
        return {
            "type": "emotional",
            "confidence": 0.5,
            "reason": "Default classification - weak emotional signal"
        }
    
    def should_skip_emotion_classification(self, message_type_result: Dict) -> bool:
        """Determine if emotion classification should be skipped"""
        msg_type = message_type_result["type"]
        confidence = message_type_result["confidence"]
        
        # Skip for high-confidence short replies
        if msg_type == "short_reply" and confidence >= 0.8:
            return True
        
        # Skip for high-confidence contextual messages
        if msg_type == "contextual" and confidence >= 0.8:
            return True
        
        return False
    
    def get_fallback_emotion(self, message_type_result: Dict, context_emotion: str = None) -> str:
        """Get fallback emotion for non-emotional messages"""
        msg_type = message_type_result["type"]
        
        if msg_type == "short_reply":
            # Use context emotion if available, otherwise neutral
            return context_emotion if context_emotion else "neutral"
        
        elif msg_type == "contextual":
            # Use context emotion if available, otherwise neutral
            return context_emotion if context_emotion else "neutral"
        
        elif msg_type == "neutral":
            return "neutral"
        
        # For emotional type, don't use fallback
        return None


# Singleton instance
_message_type_detector = None


def get_message_type_detector() -> MessageTypeDetector:
    """Get singleton message type detector instance"""
    global _message_type_detector
    if _message_type_detector is None:
        _message_type_detector = MessageTypeDetector()
    return _message_type_detector


def detect_message_type(text: str, context_available: bool = False) -> Dict[str, any]:
    """
    Convenience function to detect message type
    
    Args:
        text: User message
        context_available: Whether conversation context exists
    
    Returns:
        Dict with type, confidence, and reason
    """
    detector = get_message_type_detector()
    return detector.detect_message_type(text, context_available)
