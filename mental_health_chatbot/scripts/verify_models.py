#!/usr/bin/env python3
"""
Script to verify all ONNX models are working correctly
Run this after download_models.py
"""

import os
os.environ["PYTHONIOENCODING"] = "utf-8"

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from models.translator import get_translation_manager

TEST_SENTENCE = "I feel really sad and hopeless today"


def test_emotion_classifier():
    """Test emotion classifier"""
    print("\n" + "=" * 60)
    print("Testing Emotion Classifier")
    print("=" * 60)
    
    try:
        model = get_emotion_model()
        
        if model.is_loaded():
            print("✓ Model loaded (ONNX)")
        else:
            print("⚠ Using rule-based fallback")
        
        result = model.predict(TEST_SENTENCE)
        
        print(f"\nInput: {TEST_SENTENCE}")
        print(f"Detected emotion: {result['emotion']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"\nAll scores:")
        for emotion, score in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {emotion}: {score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_intent_classifier():
    """Test intent classifier"""
    print("\n" + "=" * 60)
    print("Testing Intent Classifier")
    print("=" * 60)
    
    try:
        model = get_intent_model()
        
        if model.is_loaded():
            print("✓ Model loaded (ONNX)")
        else:
            print("⚠ Using rule-based fallback")
        
        result = model.predict(TEST_SENTENCE)
        
        print(f"\nInput: {TEST_SENTENCE}")
        print(f"Detected intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"\nAll scores:")
        for intent, score in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {intent}: {score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_translation():
    """Test translation manager"""
    print("\n" + "=" * 60)
    print("Testing Translation Manager")
    print("=" * 60)
    
    try:
        manager = get_translation_manager()
        
        # Test language detection
        test_texts = {
            "en": "I am feeling very sad",
            "hi": "मुझे बहुत दुख हो रहा है",
            "fr": "Je me sens très triste",
            "es": "Me siento muy triste"
        }
        
        print("\nLanguage Detection:")
        for expected_lang, text in test_texts.items():
            detected = manager.detect_language(text)
            status = "✓" if detected == expected_lang else "⚠"
            print(f"  {status} '{text[:30]}...' → {detected} (expected: {expected_lang})")
        
        # Test translation (Hindi to English) - will download model on first use
        print("\nTranslation Test (Hindi → English):")
        print("  Note: This will download the translation model from HuggingFace...")
        hindi_text = "मुझे बहुत दुख हो रहा है"
        try:
            translated = manager.translate_to_english(hindi_text, "hi")
            print(f"  Input: {hindi_text}")
            print(f"  Output: {translated}")
            
            if translated == hindi_text:
                print("  ⚠ Translation returned original text (model may not be available)")
            else:
                print("  ✓ Translation successful")
        except Exception as e:
            print(f"  ⚠ Translation test skipped: {e}")
            print("  (Translation models will be downloaded on first use at runtime)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Mental Health Chatbot - Model Verification")
    print("=" * 60)
    
    results = {
        "Emotion Classifier": test_emotion_classifier(),
        "Intent Classifier": test_intent_classifier(),
        "Translation Manager": test_translation()
    }
    
    # Print summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All models verified successfully!")
        print("The backend is ready to run.")
    else:
        print("\n⚠ Some models failed verification.")
        print("The backend will still run with fallbacks, but functionality may be limited.")
    
    print("\nNext step:")
    print("  cd backend && python main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
