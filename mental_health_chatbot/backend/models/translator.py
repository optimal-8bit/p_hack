import logging
from typing import Dict, Optional
import config

logger = logging.getLogger(__name__)


class TranslationManager:
    def __init__(self):
        self.models = {}  # Lazy-loaded translation models
        self.tokenizers = {}
        self.use_onnx = {}  # Track which models use ONNX vs transformers
        
    def detect_language(self, text: str) -> tuple[str, float]:
        """Detect language of text, return (ISO 639-1 code, confidence)"""
        try:
            import langdetect
            from langdetect.lang_detect_exception import LangDetectException
            
            # Get language probabilities
            try:
                probabilities = langdetect.detect_langs(text)
                if probabilities:
                    detected = probabilities[0].lang
                    confidence = probabilities[0].prob
                else:
                    detected = "en"
                    confidence = 0.5
            except LangDetectException:
                # Fallback for very short text or detection failure
                detected = "en"
                confidence = 0.3
            
            # Map to supported languages
            if detected in config.SUPPORTED_LANGUAGES:
                return detected, confidence
            else:
                logger.info(f"Detected language '{detected}' not supported, defaulting to 'en'")
                return "en", 0.5
                
        except Exception as e:
            logger.warning(f"Language detection failed: {e}. Defaulting to 'en'")
            return "en", 0.3
    
    def translate_to_english(self, text: str, source_lang: str) -> str:
        """Translate text from source_lang to English"""
        # If already English or not supported, return as-is
        if source_lang == "en" or source_lang not in config.SUPPORTED_LANGUAGES:
            return text
        
        try:
            model_key = f"{source_lang}_to_en"
            model, tokenizer = self._get_translation_model(source_lang, "to_en")
            
            if model is None:
                logger.warning(f"Translation model {model_key} not available. Returning original text.")
                return text
            
            # Translate
            if self.use_onnx.get(model_key, False):
                return self._translate_onnx(text, model, tokenizer)
            else:
                return self._translate_transformers(text, model, tokenizer)
                
        except Exception as e:
            logger.error(f"Translation to English failed: {e}. Returning original text.")
            return text
    
    def translate_from_english(self, text: str, target_lang: str) -> str:
        """Translate text from English to target_lang"""
        # If target is English or not supported, return as-is
        if target_lang == "en" or target_lang not in config.SUPPORTED_LANGUAGES:
            return text
        
        try:
            model_key = f"en_to_{target_lang}"
            model, tokenizer = self._get_translation_model(target_lang, "from_en")
            
            if model is None:
                logger.warning(f"Translation model {model_key} not available. Returning original text.")
                return text
            
            # Translate
            if self.use_onnx.get(model_key, False):
                return self._translate_onnx(text, model, tokenizer)
            else:
                return self._translate_transformers(text, model, tokenizer)
                
        except Exception as e:
            logger.error(f"Translation from English failed: {e}. Returning original text.")
            return text
    
    def _get_translation_model(self, lang_code: str, direction: str):
        """Lazy-load translation model (transformers only, no ONNX)"""
        model_key = f"{lang_code}_{direction}"
        
        # Return cached model if already loaded
        if model_key in self.models:
            return self.models[model_key], self.tokenizers[model_key]
        
        # Get model directory
        if lang_code not in config.TRANSLATION_MODEL_DIRS:
            return None, None
        
        model_dir = config.TRANSLATION_MODEL_DIRS[lang_code][direction]
        
        # Try loading from transformers (always use transformers, not ONNX)
        try:
            from transformers import MarianMTModel, MarianTokenizer
            
            # Determine HuggingFace model ID
            if direction == "to_en":
                hf_model_id = f"Helsinki-NLP/opus-mt-{lang_code}-en"
            else:
                hf_model_id = f"Helsinki-NLP/opus-mt-en-{lang_code}"
            
            logger.info(f"Loading translation model from HuggingFace: {hf_model_id}")
            
            model = MarianMTModel.from_pretrained(hf_model_id)
            tokenizer = MarianTokenizer.from_pretrained(hf_model_id)
            
            self.models[model_key] = model
            self.tokenizers[model_key] = tokenizer
            self.use_onnx[model_key] = False
            
            logger.info(f"Loaded transformers translation model: {model_key}")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load translation model {model_key}: {e}")
            return None, None
    
    def _translate_onnx(self, text: str, model, tokenizer) -> str:
        """Translate using ONNX model (not used for translation anymore)"""
        try:
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            outputs = model.generate(**inputs)
            translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translated
        except Exception as e:
            logger.error(f"ONNX translation failed: {e}")
            return text
    
    def _translate_transformers(self, text: str, model, tokenizer) -> str:
        """Translate using transformers model"""
        try:
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            outputs = model.generate(**inputs, max_length=512)
            translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translated
        except Exception as e:
            logger.error(f"Transformers translation failed: {e}")
            return text


# Singleton instance
_translation_manager: Optional[TranslationManager] = None


def get_translation_manager() -> TranslationManager:
    """Get singleton translation manager instance"""
    global _translation_manager
    if _translation_manager is None:
        _translation_manager = TranslationManager()
    return _translation_manager
