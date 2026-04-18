import logging
from typing import List

logger = logging.getLogger(__name__)

# High emotion vocabulary
HIGH_EMOTION_WORDS = {
    # sadness
    "hopeless", "worthless", "empty", "hollow", "numb", "broken",
    "crying", "tears", "grief", "loss", "alone", "lonely", "isolated",
    "depressed", "depression", "sad", "miserable", "devastated",
    # anxiety/fear
    "scared", "terrified", "panic", "panicking", "anxious", "anxiety",
    "worried", "worry", "fear", "afraid", "dread", "nervous", "shaking",
    # anger
    "angry", "furious", "rage", "hate", "frustrated", "useless",
    "pointless", "unfair",
    # crisis
    "die", "dying", "dead", "suicide", "hurt", "pain", "suffering",
    "anymore", "never", "nothing", "nobody", "worthless",
}

MEDIUM_EMOTION_WORDS = {
    "feel", "feeling", "really", "very", "so", "always", "never", "every"
}


class WordAttributor:
    def __init__(self):
        logger.info("Word attributor initialized")
    
    def compute_text_weights(
        self,
        transcript: str,
        word_timestamps: List,
        emotion_model
    ) -> List[float]:
        """Compute text-side importance of each word"""
        words = [wt.word for wt in word_timestamps]
        
        if len(words) == 0:
            return []
        
        # Use leave-one-out for short messages, vocabulary lookup for long ones
        if len(words) <= 15:
            return self._compute_leave_one_out(transcript, words, emotion_model)
        else:
            return self._compute_vocabulary_based(words)
    
    def _compute_leave_one_out(
        self,
        transcript: str,
        words: List[str],
        emotion_model
    ) -> List[float]:
        """Leave-one-out attribution for short messages"""
        try:
            # Get baseline confidence
            baseline_result = emotion_model.predict(transcript)
            baseline_confidence = baseline_result["confidence"]
            
            weights = []
            for i in range(len(words)):
                # Create text without this word
                words_without = words[:i] + words[i+1:]
                text_without = " ".join(words_without)
                
                if not text_without.strip():
                    # If removing this word leaves empty text, it's important
                    weights.append(1.0)
                    continue
                
                # Get confidence without this word
                result_without = emotion_model.predict(text_without)
                confidence_without = result_without["confidence"]
                
                # Weight is how much confidence dropped
                raw_weight = max(0.0, baseline_confidence - confidence_without)
                weights.append(raw_weight)
            
            # Normalize to 0-1 range
            if weights:
                max_weight = max(weights)
                if max_weight > 0:
                    weights = [w / max_weight for w in weights]
                else:
                    weights = [0.5] * len(weights)
            
            return weights
            
        except Exception as e:
            logger.error(f"Leave-one-out attribution failed: {e}", exc_info=True)
            # Fallback to vocabulary-based
            return self._compute_vocabulary_based(words)
    
    def _compute_vocabulary_based(self, words: List[str]) -> List[float]:
        """Vocabulary-based attribution for long messages"""
        weights = []
        
        for word in words:
            word_lower = word.lower().strip()
            
            if word_lower in HIGH_EMOTION_WORDS:
                weight = 0.9
            elif word_lower in MEDIUM_EMOTION_WORDS:
                weight = 0.5
            else:
                weight = 0.1
            
            weights.append(weight)
        
        # Normalize to 0-1 range
        if weights:
            max_weight = max(weights)
            if max_weight > 0:
                weights = [w / max_weight for w in weights]
            else:
                weights = [0.5] * len(weights)
        
        return weights


# Singleton instance
_word_attributor = None


def get_word_attributor() -> WordAttributor:
    """Get singleton word attributor instance"""
    global _word_attributor
    if _word_attributor is None:
        _word_attributor = WordAttributor()
    return _word_attributor
