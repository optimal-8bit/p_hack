import logging
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import config

logger = logging.getLogger(__name__)

# Rule-based fallback emotions
RULE_BASED_EMOTIONS = {
    "sadness": ["sad", "cry", "crying", "depressed", "depression", "hopeless", "empty", "worthless", "miserable", "grief", "lost", "broken"],
    "fear": ["scared", "afraid", "terrified", "panic", "anxious", "anxiety", "worried", "worry", "nervous", "dread", "phobia"],
    "anger": ["angry", "furious", "rage", "hate", "frustrated", "frustration", "annoyed", "irritated", "mad"],
    "joy": ["happy", "excited", "great", "wonderful", "amazing", "good", "fantastic", "love", "grateful", "blessed"],
    "surprise": ["shocked", "surprised", "unexpected", "unbelievable", "wow", "omg"],
}


class EmotionClassifier:
    def __init__(self):
        self.session = None
        self.tokenizer = None
        self.use_onnx = False
        self._load_model()
    
    def _load_model(self):
        """Load ONNX model or fall back to rule-based"""
        try:
            import onnxruntime as ort
            from transformers import AutoTokenizer
            
            model_path = config.EMOTION_MODEL_DIR / "model.onnx"
            
            if not model_path.exists():
                logger.warning(f"ONNX emotion model not found at {model_path}. Using rule-based fallback.")
                return
            
            # Load ONNX session
            self.session = ort.InferenceSession(
                str(model_path),
                providers=["CPUExecutionProvider"]
            )
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(str(config.EMOTION_MODEL_DIR))
            
            self.use_onnx = True
            logger.info("Emotion classifier ONNX model loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load ONNX emotion model: {e}. Using rule-based fallback.")
            self.use_onnx = False
    
    def is_loaded(self) -> bool:
        """Check if ONNX model is loaded"""
        return self.use_onnx and self.session is not None
    
    def predict(self, text: str) -> Dict:
        """Predict emotion from text"""
        if self.use_onnx and self.session is not None:
            return self._predict_onnx(text)
        else:
            return self._predict_rule_based(text)
    
    def _predict_onnx(self, text: str) -> Dict:
        """ONNX-based prediction"""
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                max_length=128,
                truncation=True,
                padding="max_length",
                return_tensors="np"
            )
            
            # Get input names
            input_names = [inp.name for inp in self.session.get_inputs()]
            
            # Prepare feed dict
            feed_dict = {}
            if "input_ids" in input_names:
                feed_dict["input_ids"] = inputs["input_ids"].astype(np.int64)
            if "attention_mask" in input_names:
                feed_dict["attention_mask"] = inputs["attention_mask"].astype(np.int64)
            
            # Run inference
            outputs = self.session.run(None, feed_dict)
            logits = outputs[0][0]  # First output, first batch
            
            # Apply softmax
            exp_logits = np.exp(logits - np.max(logits))
            probabilities = exp_logits / exp_logits.sum()
            
            # Map to emotion labels
            all_scores = {
                emotion: float(probabilities[i])
                for i, emotion in enumerate(config.EMOTION_LABELS)
            }
            
            # Get top emotion
            top_idx = np.argmax(probabilities)
            top_emotion = config.EMOTION_LABELS[top_idx]
            top_confidence = float(probabilities[top_idx])
            
            return {
                "emotion": top_emotion,
                "confidence": top_confidence,
                "all_scores": all_scores
            }
            
        except Exception as e:
            logger.error(f"ONNX emotion prediction failed: {e}. Falling back to rule-based.")
            return self._predict_rule_based(text)
    
    def _predict_rule_based(self, text: str) -> Dict:
        """Rule-based fallback prediction"""
        text_lower = text.lower()
        
        # Count keyword hits for each emotion
        emotion_scores = {}
        for emotion, keywords in RULE_BASED_EMOTIONS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Add disgust (not in rule-based keywords)
        emotion_scores["disgust"] = 0
        
        # Find max score
        max_score = max(emotion_scores.values())
        
        if max_score == 0:
            # Default to neutral
            top_emotion = "neutral"
            top_confidence = 0.5
        else:
            # Get emotion with highest score
            top_emotion = max(emotion_scores, key=emotion_scores.get)
            # Normalize confidence (simple heuristic)
            top_confidence = min(0.3 + (max_score * 0.15), 0.95)
        
        # Create normalized scores for all emotions
        total = sum(emotion_scores.values()) or 1
        all_scores = {
            emotion: score / total if total > 0 else (1.0 if emotion == top_emotion else 0.0)
            for emotion, score in emotion_scores.items()
        }
        
        # Ensure all config emotions are present
        for emotion in config.EMOTION_LABELS:
            if emotion not in all_scores:
                all_scores[emotion] = 0.0
        
        return {
            "emotion": top_emotion,
            "confidence": top_confidence,
            "all_scores": all_scores
        }


# Singleton instance
_emotion_model: Optional[EmotionClassifier] = None


def get_emotion_model() -> EmotionClassifier:
    """Get singleton emotion classifier instance"""
    global _emotion_model
    if _emotion_model is None:
        _emotion_model = EmotionClassifier()
    return _emotion_model
