"""
Multimodal Emotion Fusion
Combines text-based emotion with facial emotion from webcam
"""
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)


# Emotion mapping between different systems
EMOTION_MAPPING = {
    # face-api.js emotions -> our system
    "happy": "joy",
    "sad": "sadness",
    "angry": "anger",
    "fearful": "fear",
    "disgusted": "disgust",
    "surprised": "surprise",
    "neutral": "neutral"
}

# Reverse mapping
REVERSE_EMOTION_MAPPING = {v: k for k, v in EMOTION_MAPPING.items()}


def normalize_facial_emotion(facial_emotion: str) -> str:
    """Convert face-api.js emotion to our system's emotion labels"""
    return EMOTION_MAPPING.get(facial_emotion.lower(), facial_emotion)


def calculate_emotion_congruence(
    text_emotion: str,
    facial_emotion: str,
    text_confidence: float,
    facial_confidence: float
) -> Tuple[str, float]:
    """
    Determine if text and facial emotions are congruent
    
    Returns:
        (congruence_status, incongruence_score)
        congruence_status: "congruent", "incongruent", "uncertain"
        incongruence_score: 0.0 to 1.0 (higher = more incongruent)
    """
    # Normalize facial emotion to our system
    normalized_facial = normalize_facial_emotion(facial_emotion)
    
    # If both emotions are the same
    if text_emotion.lower() == normalized_facial.lower():
        return "congruent", 0.0
    
    # Define emotion groups (similar emotions)
    emotion_groups = [
        {"joy", "happy", "surprise"},
        {"sadness", "sad", "fear", "fearful"},
        {"anger", "angry", "disgust", "disgusted"},
        {"neutral"}
    ]
    
    # Check if emotions are in the same group
    text_lower = text_emotion.lower()
    facial_lower = normalized_facial.lower()
    
    for group in emotion_groups:
        if text_lower in group and facial_lower in group:
            return "congruent", 0.2  # Slightly incongruent but same family
    
    # If confidences are low, mark as uncertain
    if text_confidence < 0.5 or facial_confidence < 0.5:
        return "uncertain", 0.3
    
    # Calculate incongruence score based on confidence levels
    avg_confidence = (text_confidence + facial_confidence) / 2
    incongruence_score = avg_confidence * 0.7  # High confidence + different emotions = high incongruence
    
    return "incongruent", incongruence_score


def fuse_emotions(
    text_emotion: str,
    text_confidence: float,
    facial_emotion: Optional[str] = None,
    facial_confidence: Optional[float] = None,
    facial_all_scores: Optional[Dict[str, float]] = None
) -> Dict:
    """
    Fuse text-based and facial emotions using weighted averaging
    
    Strategy:
    - If only text emotion available, use it
    - If both available, use weighted average (text 60%, facial 40%)
    - Detect incongruence for mental health insights
    
    Returns:
        {
            "fused_emotion": str,
            "fused_confidence": float,
            "facial_emotion": str or None,
            "facial_confidence": float or None,
            "is_multimodal": bool,
            "congruence": str or None,
            "incongruence_score": float or None,
            "fusion_note": str
        }
    """
    # If no facial emotion, return text-only
    if not facial_emotion or facial_confidence is None:
        return {
            "fused_emotion": text_emotion,
            "fused_confidence": text_confidence,
            "facial_emotion": None,
            "facial_confidence": None,
            "is_multimodal": False,
            "congruence": None,
            "incongruence_score": None,
            "fusion_note": "Text-only emotion analysis"
        }
    
    # Normalize facial emotion
    normalized_facial = normalize_facial_emotion(facial_emotion)
    
    # Calculate congruence
    congruence, incongruence_score = calculate_emotion_congruence(
        text_emotion, facial_emotion, text_confidence, facial_confidence
    )
    
    # Fusion strategy based on congruence
    if congruence == "congruent":
        # Both agree - boost confidence
        fused_emotion = text_emotion
        fused_confidence = min(0.99, (text_confidence + facial_confidence) / 2 * 1.2)
        fusion_note = f"Text and facial emotions agree ({text_emotion})"
        
    elif congruence == "incongruent":
        # Emotions disagree - this is valuable information!
        # Use text emotion but flag the incongruence
        if text_confidence > facial_confidence:
            fused_emotion = text_emotion
            fused_confidence = text_confidence * 0.9  # Slightly reduce confidence
            fusion_note = f"Incongruence detected: text shows {text_emotion}, face shows {facial_emotion}"
        else:
            fused_emotion = normalized_facial
            fused_confidence = facial_confidence * 0.9
            fusion_note = f"Incongruence detected: face shows {facial_emotion}, text shows {text_emotion}"
    
    else:  # uncertain
        # Low confidence - use weighted average
        if text_confidence > facial_confidence:
            fused_emotion = text_emotion
            fused_confidence = text_confidence * 0.7 + facial_confidence * 0.3
        else:
            fused_emotion = normalized_facial
            fused_confidence = facial_confidence * 0.6 + text_confidence * 0.4
        fusion_note = "Low confidence - using weighted fusion"
    
    logger.info(
        f"Emotion fusion: text={text_emotion}({text_confidence:.2f}), "
        f"facial={facial_emotion}({facial_confidence:.2f}), "
        f"fused={fused_emotion}({fused_confidence:.2f}), "
        f"congruence={congruence}"
    )
    
    return {
        "fused_emotion": fused_emotion,
        "fused_confidence": fused_confidence,
        "facial_emotion": facial_emotion,
        "facial_confidence": facial_confidence,
        "is_multimodal": True,
        "congruence": congruence,
        "incongruence_score": incongruence_score,
        "fusion_note": fusion_note
    }
