import logging
from dataclasses import dataclass
from typing import List
from collections import Counter

logger = logging.getLogger(__name__)

# Emotion valence mapping for incongruence detection
EMOTION_VALENCE = {
    "sadness": -1,
    "fear": -1,
    "anger": -1,
    "disgust": -1,
    "joy": 1,
    "surprise": 0,
    "neutral": 0
}


@dataclass
class FusedWordResult:
    word: str
    final_weight: float          # 0-1 combined importance
    text_weight: float           # from leave-one-out or vocabulary
    audio_weight: float          # from audio analyzer
    pitch_normalized: float
    amplitude_normalized: float
    is_stressed: bool
    emotion_hint: str            # from audio


@dataclass
class FusionResult:
    word_results: List[FusedWordResult]
    
    text_only_emotion: str
    text_only_confidence: float
    audio_focused_emotion: str
    audio_focused_confidence: float
    fused_emotion: str
    fused_confidence: float
    
    intent: str
    intent_confidence: float
    
    is_incongruent: bool
    incongruence_score: float
    incongruence_note: str
    
    stressed_words: List[str]    # words with final_weight > 0.6


class FusionEngine:
    def __init__(self):
        logger.info("Fusion engine initialized")
    
    def fuse(
        self,
        transcript: str,
        word_timestamps: List,
        text_weights: List[float],
        audio_features: List,
        emotion_model,
        intent_model
    ) -> FusionResult:
        """Fuse audio and text signals for enhanced emotion detection"""
        try:
            # Step 1: Compute per-word final weights
            word_results = []
            for i, wt in enumerate(word_timestamps):
                text_weight = text_weights[i] if i < len(text_weights) else 0.5
                audio_feat = audio_features[i] if i < len(audio_features) else None
                
                if audio_feat:
                    audio_weight = audio_feat.audio_weight
                    final_weight = (text_weight * 0.50) + (audio_weight * 0.50)
                    
                    word_results.append(FusedWordResult(
                        word=wt.word,
                        final_weight=final_weight,
                        text_weight=text_weight,
                        audio_weight=audio_weight,
                        pitch_normalized=audio_feat.pitch_normalized,
                        amplitude_normalized=audio_feat.amplitude_normalized,
                        is_stressed=audio_feat.is_stressed,
                        emotion_hint=audio_feat.emotion_hint
                    ))
                else:
                    # No audio features, use text weight only
                    word_results.append(FusedWordResult(
                        word=wt.word,
                        final_weight=text_weight,
                        text_weight=text_weight,
                        audio_weight=0.5,
                        pitch_normalized=0.5,
                        amplitude_normalized=0.5,
                        is_stressed=False,
                        emotion_hint="neutral"
                    ))
            
            # Step 2: Two-stage emotion classification
            # Stage 1: Full transcript
            text_result = emotion_model.predict(transcript)
            text_emotion = text_result["emotion"]
            text_confidence = text_result["confidence"]
            
            # Stage 2: High-weight words only
            high_weight_words = [
                wr.word for wr in word_results if wr.final_weight > 0.55
            ]
            
            if len(high_weight_words) >= 2:
                focused_text = " ".join(high_weight_words)
                audio_focused_result = emotion_model.predict(focused_text)
                audio_focused_emotion = audio_focused_result["emotion"]
                audio_focused_confidence = audio_focused_result["confidence"]
            else:
                # Not enough signal — fall back to full text result
                audio_focused_emotion = text_emotion
                audio_focused_confidence = text_confidence
            
            # Stage 3: Fuse emotions
            if audio_focused_emotion == text_emotion:
                fused_emotion = text_emotion
                fused_confidence = (text_confidence * 0.40) + (audio_focused_confidence * 0.60)
            else:
                # Disagreement — pick higher confidence, apply penalty
                if audio_focused_confidence >= text_confidence:
                    fused_emotion = audio_focused_emotion
                    fused_confidence = audio_focused_confidence * 0.85
                else:
                    fused_emotion = text_emotion
                    fused_confidence = text_confidence * 0.85
            
            # Step 3: Intent always uses full transcript
            intent_result = intent_model.predict(transcript)
            
            # Step 4: Incongruence detection
            audio_emotions = [
                wr.emotion_hint for wr in word_results
                if wr.emotion_hint != "neutral"
            ]
            
            if audio_emotions:
                # Get most common audio emotion
                emotion_counter = Counter(audio_emotions)
                dominant_audio_emotion = emotion_counter.most_common(1)[0][0]
            else:
                dominant_audio_emotion = "neutral"
            
            # Map audio emotion hints to standard emotion labels
            audio_emotion_mapped = self._map_audio_emotion(dominant_audio_emotion)
            
            text_valence = EMOTION_VALENCE.get(text_emotion, 0)
            audio_valence = EMOTION_VALENCE.get(audio_emotion_mapped, 0)
            
            incongruence_score = abs(text_valence - audio_valence) / 2.0
            is_incongruent = incongruence_score > 0.4
            
            if is_incongruent:
                incongruence_note = (
                    f"Your words suggest {text_emotion} but your voice patterns suggest "
                    f"{dominant_audio_emotion}. This contrast can sometimes indicate masked distress."
                )
            else:
                incongruence_note = ""
            
            # Get stressed words
            stressed_words = [wr.word for wr in word_results if wr.final_weight > 0.6]
            
            return FusionResult(
                word_results=word_results,
                text_only_emotion=text_emotion,
                text_only_confidence=text_confidence,
                audio_focused_emotion=audio_focused_emotion,
                audio_focused_confidence=audio_focused_confidence,
                fused_emotion=fused_emotion,
                fused_confidence=fused_confidence,
                intent=intent_result["intent"],
                intent_confidence=intent_result["confidence"],
                is_incongruent=is_incongruent,
                incongruence_score=incongruence_score,
                incongruence_note=incongruence_note,
                stressed_words=stressed_words
            )
            
        except Exception as e:
            logger.error(f"Fusion failed: {e}", exc_info=True)
            raise
    
    def _map_audio_emotion(self, audio_hint: str) -> str:
        """Map audio emotion hints to standard emotion labels"""
        mapping = {
            "anxiety": "fear",
            "sadness": "sadness",
            "anger": "anger",
            "dissociation": "neutral",
            "neutral": "neutral"
        }
        return mapping.get(audio_hint, "neutral")


# Singleton instance
_fusion_engine = None


def get_fusion_engine() -> FusionEngine:
    """Get singleton fusion engine instance"""
    global _fusion_engine
    if _fusion_engine is None:
        _fusion_engine = FusionEngine()
    return _fusion_engine
