import logging
import librosa
import numpy as np
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ClipBaseline:
    pitch_mean: float
    pitch_std: float
    amplitude_mean: float
    amplitude_std: float
    speech_rate: float


@dataclass
class WordAudioFeatures:
    word: str
    pitch_normalized: float      # 0-1 relative to baseline
    amplitude_normalized: float  # 0-1 relative to baseline
    pitch_deviation: float       # how far from speaker's normal pitch
    is_stressed: bool            # True if amplitude > baseline + 1.5*std
    audio_weight: float          # combined 0-1 importance score
    emotion_hint: str            # anxiety/sadness/anger/neutral/dissociation


class AudioAnalyzer:
    def __init__(self):
        logger.info("Audio analyzer initialized")
    
    def analyze_clip(self, audio_path: str) -> ClipBaseline:
        """Analyze full audio clip to get speaker baseline"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=16000)
            
            # Extract pitch using YIN algorithm
            pitches = librosa.yin(y, fmin=50, fmax=400, sr=sr)
            # Filter out NaN values
            valid_pitches = pitches[~np.isnan(pitches)]
            
            if len(valid_pitches) > 0:
                pitch_mean = float(np.mean(valid_pitches))
                pitch_std = float(np.std(valid_pitches))
            else:
                pitch_mean = 150.0  # Default neutral pitch
                pitch_std = 20.0
            
            # Extract amplitude (RMS energy)
            rms = librosa.feature.rms(y=y)[0]
            amplitude_mean = float(np.mean(rms))
            amplitude_std = float(np.std(rms))
            
            # Estimate speech rate (words per second would be calculated externally)
            duration = len(y) / sr
            speech_rate = duration  # Placeholder, actual rate computed with word count
            
            return ClipBaseline(
                pitch_mean=pitch_mean,
                pitch_std=pitch_std,
                amplitude_mean=amplitude_mean,
                amplitude_std=amplitude_std,
                speech_rate=speech_rate
            )
            
        except Exception as e:
            logger.error(f"Failed to analyze clip baseline: {e}", exc_info=True)
            # Return safe defaults
            return ClipBaseline(
                pitch_mean=150.0,
                pitch_std=20.0,
                amplitude_mean=0.1,
                amplitude_std=0.05,
                speech_rate=1.0
            )
    
    def analyze_word(
        self,
        audio_path: str,
        start: float,
        end: float,
        baseline: ClipBaseline,
        word: str
    ) -> WordAudioFeatures:
        """Analyze audio features for a specific word"""
        try:
            # Ensure minimum duration
            duration = max(end - start, 0.1)
            
            # Load word segment
            y, sr = librosa.load(audio_path, sr=16000, offset=start, duration=duration)
            
            # Handle empty or very short segments
            if len(y) < 100:
                return self._get_safe_defaults(word)
            
            # Extract pitch
            pitches = librosa.yin(y, fmin=50, fmax=400, sr=sr)
            valid_pitches = pitches[~np.isnan(pitches)]
            
            if len(valid_pitches) > 0:
                pitch_value = float(np.mean(valid_pitches))
            else:
                pitch_value = baseline.pitch_mean
            
            # Extract amplitude
            rms = librosa.feature.rms(y=y)[0]
            amplitude_value = float(np.mean(rms))
            
            # Normalize relative to baseline
            pitch_normalized = self._normalize(
                pitch_value,
                baseline.pitch_mean - baseline.pitch_std,
                baseline.pitch_mean + baseline.pitch_std
            )
            
            amplitude_normalized = self._normalize(
                amplitude_value,
                baseline.amplitude_mean - baseline.amplitude_std,
                baseline.amplitude_mean + baseline.amplitude_std
            )
            
            # Calculate pitch deviation
            pitch_deviation = abs(pitch_value - baseline.pitch_mean) / (baseline.pitch_std + 1e-6)
            pitch_deviation = min(pitch_deviation, 1.0)
            
            # Determine if stressed
            is_stressed = amplitude_value > (baseline.amplitude_mean + 1.5 * baseline.amplitude_std)
            
            # Calculate audio weight
            audio_weight = (
                amplitude_normalized * 0.40 +
                pitch_deviation * 0.35 +
                (1.0 if is_stressed else 0.0) * 0.25
            )
            audio_weight = max(0.0, min(1.0, audio_weight))
            
            # Determine emotion hint
            emotion_hint = self._get_emotion_hint(
                pitch_normalized,
                amplitude_normalized,
                pitch_deviation
            )
            
            return WordAudioFeatures(
                word=word,
                pitch_normalized=pitch_normalized,
                amplitude_normalized=amplitude_normalized,
                pitch_deviation=pitch_deviation,
                is_stressed=is_stressed,
                audio_weight=audio_weight,
                emotion_hint=emotion_hint
            )
            
        except Exception as e:
            logger.warning(f"Failed to analyze word '{word}': {e}")
            return self._get_safe_defaults(word)
    
    def _normalize(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize value to 0-1 range"""
        if max_val - min_val < 1e-6:
            return 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))
    
    def _get_emotion_hint(
        self,
        pitch_normalized: float,
        amplitude_normalized: float,
        pitch_deviation: float
    ) -> str:
        """Determine emotion hint from audio features"""
        if pitch_normalized > 0.7 and amplitude_normalized > 0.65:
            return "anger"
        elif pitch_normalized > 0.65 and pitch_deviation > 0.6:
            return "anxiety"
        elif pitch_normalized < 0.35 and amplitude_normalized < 0.4:
            return "sadness"
        elif amplitude_normalized < 0.3 and pitch_deviation < 0.2:
            return "dissociation"  # flat affect — clinically important
        else:
            return "neutral"
    
    def _get_safe_defaults(self, word: str) -> WordAudioFeatures:
        """Return safe default features when analysis fails"""
        return WordAudioFeatures(
            word=word,
            pitch_normalized=0.5,
            amplitude_normalized=0.5,
            pitch_deviation=0.5,
            is_stressed=False,
            audio_weight=0.5,
            emotion_hint="neutral"
        )


# Singleton instance
_audio_analyzer: Optional[AudioAnalyzer] = None


def get_audio_analyzer() -> AudioAnalyzer:
    """Get singleton audio analyzer instance"""
    global _audio_analyzer
    if _audio_analyzer is None:
        _audio_analyzer = AudioAnalyzer()
    return _audio_analyzer
