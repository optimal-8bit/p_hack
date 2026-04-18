# All paths and constants live here — never hardcode in other files

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
ONNX_MODELS_DIR = BASE_DIR / "onnx_models"

# Model paths
EMOTION_MODEL_DIR = ONNX_MODELS_DIR / "emotion_classifier"
INTENT_MODEL_DIR = ONNX_MODELS_DIR / "intent_classifier"

# Translation model directories mapped by language code
TRANSLATION_MODEL_DIRS = {
    "hi": {
        "to_en": ONNX_MODELS_DIR / "translate_hi_en",
        "from_en": ONNX_MODELS_DIR / "translate_en_hi",
    },
    "fr": {
        "to_en": ONNX_MODELS_DIR / "translate_fr_en",
        "from_en": ONNX_MODELS_DIR / "translate_en_fr",
    },
    "es": {
        "to_en": ONNX_MODELS_DIR / "translate_es_en",
        "from_en": ONNX_MODELS_DIR / "translate_en_es",
    },
}

# Supported languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = ["en", "hi", "fr", "es"]

# Intent labels used for zero-shot classification
INTENT_LABELS = [
    "anxiety and panic",
    "sadness and depression",
    "stress and overwhelm",
    "loneliness and isolation",
    "anger and frustration",
    "general emotional support",
]

# Emotion labels (must match j-hartmann model output exactly)
EMOTION_LABELS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

# Conversation context window
CONTEXT_WINDOW_SIZE = 5

# Safety: these trigger immediate crisis response (case-insensitive, regex)
CRISIS_PATTERNS = [
    r"\b(suicid\w*)\b",
    r"\b(want to die|wanna die|wish i was dead)\b",
    r"\b(kill myself|end my life|end it all)\b",
    r"\b(self.?harm|cut myself|hurt myself)\b",
    r"\b(no reason to live|can't go on)\b",
    r"\b(overdose|take all my pills)\b",
]

# Database
DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/chat_history.db"

# LLM Integration Settings
# Using Gemini API for prescription analysis (fast and reliable)
LLM_ENABLED = True  # Enabled for prescription analysis
LLM_TIMEOUT = 10.0  # Timeout for Gemini API calls
LLM_MODEL_NAME = "gemini-2.5-flash"  # Gemini model for prescription analysis
LLM_MAX_TOKENS = 200  # Max tokens for generation
LLM_TEMPERATURE = 0.3

# Server
HOST = "0.0.0.0"
PORT = 8000
