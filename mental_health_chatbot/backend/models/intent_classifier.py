import logging
import numpy as np
from typing import Dict, Optional
import config

logger = logging.getLogger(__name__)

# Rule-based fallback intents
RULE_BASED_INTENTS = {
    "anxiety and panic": ["anxious", "anxiety", "panic", "worried", "nervous", "dread", "fear", "scared"],
    "sadness and depression": ["sad", "depressed", "depression", "hopeless", "empty", "cry", "lonely", "alone"],
    "stress and overwhelm": ["stressed", "stress", "overwhelmed", "too much", "can't cope", "exhausted", "burnout"],
    "loneliness and isolation": ["lonely", "alone", "isolated", "no one", "nobody", "friendless", "abandoned"],
    "anger and frustration": ["angry", "frustrated", "rage", "furious", "hate", "annoyed"],
}


class IntentClassifier:
    def __init__(self):
        self.session = None
        self.tokenizer = None
        self.use_onnx = False
        self._load_model()
    
    def _load_model(self):
        """Load ONNX NLI model or fall back to rule-based"""
        try:
            import onnxruntime as ort
            from transformers import AutoTokenizer
            
            model_path = config.INTENT_MODEL_DIR / "model.onnx"
            
            if not model_path.exists():
                logger.warning(f"ONNX intent model not found at {model_path}. Using rule-based fallback.")
                return
            
            # Load ONNX session
            self.session = ort.InferenceSession(
                str(model_path),
                providers=["CPUExecutionProvider"]
            )
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(str(config.INTENT_MODEL_DIR))
            
            self.use_onnx = True
            logger.info("Intent classifier ONNX model loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load ONNX intent model: {e}. Using rule-based fallback.")
            self.use_onnx = False
    
    def is_loaded(self) -> bool:
        """Check if ONNX model is loaded"""
        return self.use_onnx and self.session is not None
    
    def predict(self, text: str) -> Dict:
        """Predict intent from text"""
        if self.use_onnx and self.session is not None:
            return self._predict_onnx(text)
        else:
            return self._predict_rule_based(text)
    
    def _predict_onnx(self, text: str) -> Dict:
        """ONNX-based zero-shot classification using NLI"""
        try:
            intent_scores = {}
            
            # Run NLI for each intent label
            for intent_label in config.INTENT_LABELS:
                # Create hypothesis
                hypothesis = f"This person is experiencing {intent_label}"
                
                # Tokenize premise-hypothesis pair
                inputs = self.tokenizer(
                    text,
                    hypothesis,
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
                if "token_type_ids" in input_names and "token_type_ids" in inputs:
                    feed_dict["token_type_ids"] = inputs["token_type_ids"].astype(np.int64)
                
                # Run inference
                outputs = self.session.run(None, feed_dict)
                logits = outputs[0][0]  # First output, first batch
                
                # Apply softmax
                exp_logits = np.exp(logits - np.max(logits))
                probabilities = exp_logits / exp_logits.sum()
                
                # For NLI models: [contradiction, neutral, entailment]
                # We use entailment score as intent confidence
                entailment_score = float(probabilities[-1]) if len(probabilities) >= 3 else float(probabilities[0])
                intent_scores[intent_label] = entailment_score
            
            # Normalize scores
            total = sum(intent_scores.values())
            if total > 0:
                intent_scores = {k: v / total for k, v in intent_scores.items()}
            
            # Get top intent
            top_intent = max(intent_scores, key=intent_scores.get)
            top_confidence = intent_scores[top_intent]
            
            return {
                "intent": top_intent,
                "confidence": top_confidence,
                "all_scores": intent_scores
            }
            
        except Exception as e:
            logger.error(f"ONNX intent prediction failed: {e}. Falling back to rule-based.")
            return self._predict_rule_based(text)
    
    def _predict_rule_based(self, text: str) -> Dict:
        """Rule-based fallback prediction"""
        text_lower = text.lower()
        
        # Count keyword hits for each intent
        intent_scores = {}
        for intent, keywords in RULE_BASED_INTENTS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            intent_scores[intent] = score
        
        # Add general emotional support (default)
        intent_scores["general emotional support"] = 0
        
        # Find max score
        max_score = max(intent_scores.values())
        
        if max_score == 0:
            # Default to general emotional support
            top_intent = "general emotional support"
            top_confidence = 0.5
        else:
            # Get intent with highest score
            top_intent = max(intent_scores, key=intent_scores.get)
            # Normalize confidence
            top_confidence = min(0.3 + (max_score * 0.15), 0.95)
        
        # Create normalized scores
        total = sum(intent_scores.values()) or 1
        all_scores = {
            intent: score / total if total > 0 else (1.0 if intent == top_intent else 0.0)
            for intent, score in intent_scores.items()
        }
        
        # Ensure all config intents are present
        for intent in config.INTENT_LABELS:
            if intent not in all_scores:
                all_scores[intent] = 0.0
        
        return {
            "intent": top_intent,
            "confidence": top_confidence,
            "all_scores": all_scores
        }


# Singleton instance
_intent_model: Optional[IntentClassifier] = None


def get_intent_model() -> IntentClassifier:
    """Get singleton intent classifier instance"""
    global _intent_model
    if _intent_model is None:
        _intent_model = IntentClassifier()
    return _intent_model
