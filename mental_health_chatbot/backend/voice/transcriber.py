import logging
import whisper
from dataclasses import dataclass
from typing import Optional, List

logger = logging.getLogger(__name__)


@dataclass
class WordTimestamp:
    word: str
    start: float
    end: float


@dataclass
class TranscriptionResult:
    text: str
    language: str
    words: List[WordTimestamp]
    duration_seconds: float


class Transcriber:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            logger.info("Loading Whisper model (small)... This may take a moment on first run (~460MB download)")
            self.model = whisper.load_model("small", device="cpu")
            logger.info("✓ Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.model = None
    
    def is_loaded(self) -> bool:
        """Check if Whisper model is loaded"""
        return self.model is not None
    
    def transcribe(self, audio_path: str) -> TranscriptionResult:
        """Transcribe audio file with word timestamps"""
        if not self.is_loaded():
            raise RuntimeError("Whisper model not loaded")
        
        try:
            # Transcribe with word timestamps
            result = self.model.transcribe(
                audio_path,
                word_timestamps=True,
                fp16=False
            )
            
            # Extract words from segments
            words = []
            for segment in result.get("segments", []):
                segment_words = segment.get("words", [])
                if segment_words:
                    # Use actual word timestamps
                    for word_info in segment_words:
                        words.append(WordTimestamp(
                            word=word_info.get("word", "").strip(),
                            start=word_info.get("start", 0.0),
                            end=word_info.get("end", 0.0)
                        ))
                else:
                    # Fallback: estimate evenly spaced timestamps from segment timing
                    segment_text = segment.get("text", "").strip()
                    segment_words_list = segment_text.split()
                    segment_start = segment.get("start", 0.0)
                    segment_end = segment.get("end", segment_start + 1.0)
                    segment_duration = segment_end - segment_start
                    
                    if segment_words_list:
                        word_duration = segment_duration / len(segment_words_list)
                        for i, word in enumerate(segment_words_list):
                            word_start = segment_start + (i * word_duration)
                            word_end = word_start + word_duration
                            words.append(WordTimestamp(
                                word=word,
                                start=word_start,
                                end=word_end
                            ))
            
            # Get duration
            duration = result.get("duration", 0.0)
            if duration == 0.0 and words:
                duration = words[-1].end
            
            return TranscriptionResult(
                text=result.get("text", "").strip(),
                language=result.get("language", "en"),
                words=words,
                duration_seconds=duration
            )
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            raise


# Singleton instance
_transcriber: Optional[Transcriber] = None


def get_transcriber() -> Transcriber:
    """Get singleton transcriber instance"""
    global _transcriber
    if _transcriber is None:
        _transcriber = Transcriber()
    return _transcriber
