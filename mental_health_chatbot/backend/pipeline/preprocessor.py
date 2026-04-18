import re
import logging
import unicodedata
from dataclasses import dataclass
from models.translator import get_translation_manager

logger = logging.getLogger(__name__)


@dataclass
class PreprocessedText:
    original: str
    cleaned: str
    language: str  # ISO 639-1
    was_translated: bool
    english_text: str  # text in English, ready for model inference


class Preprocessor:
    def __init__(self):
        self.translator = get_translation_manager()
        self.url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')
        self.whitespace_pattern = re.compile(r'\s+')
    
    def preprocess(self, text: str) -> PreprocessedText:
        """Clean and prepare text for model inference"""
        original = text
        
        # 1. Strip leading/trailing whitespace
        cleaned = text.strip()
        
        # 2. Normalize unicode (NFKC normalization)
        cleaned = unicodedata.normalize('NFKC', cleaned)
        
        # 3. Remove URLs
        cleaned = self.url_pattern.sub('', cleaned)
        
        # 4. Remove excessive whitespace
        cleaned = self.whitespace_pattern.sub(' ', cleaned)
        
        # 5. Truncate to 512 characters max
        if len(cleaned) > 512:
            cleaned = cleaned[:512]
            logger.info("Text truncated to 512 characters")
        
        # 6. Detect language with confidence
        detected_lang, lang_confidence = self.translator.detect_language(cleaned)
        logger.info(f"Detected language: {detected_lang} (confidence: {lang_confidence:.2f})")
        
        # 7. Translate to English if needed (skip if low confidence)
        was_translated = False
        english_text = cleaned
        
        # Skip translation if confidence is too low (likely Hinglish or mixed language)
        if detected_lang != "en" and lang_confidence >= 0.6:
            english_text = self.translator.translate_to_english(cleaned, detected_lang)
            was_translated = True
            logger.info(f"Translated from {detected_lang} to English")
        elif detected_lang != "en" and lang_confidence < 0.6:
            logger.info(f"Skipping translation due to low confidence ({lang_confidence:.2f}), processing as English")
            detected_lang = "en"  # Process as English
        
        return PreprocessedText(
            original=original,
            cleaned=cleaned,
            language=detected_lang,
            was_translated=was_translated,
            english_text=english_text
        )


# Singleton instance
_preprocessor = None


def get_preprocessor() -> Preprocessor:
    """Get singleton preprocessor instance"""
    global _preprocessor
    if _preprocessor is None:
        _preprocessor = Preprocessor()
    return _preprocessor
