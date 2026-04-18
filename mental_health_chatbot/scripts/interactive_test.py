#!/usr/bin/env python3
"""
Interactive testing script - test models with your own queries
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
from pipeline.safety import get_safety_checker
from pipeline.preprocessor import get_preprocessor


def test_query(query: str):
    """Test a single query through the pipeline"""
    print("\n" + "=" * 60)
    print(f"Testing: {query}")
    print("=" * 60)
    
    # 1. Safety check
    print("\n1. Safety Check:")
    safety_checker = get_safety_checker()
    safety_result = safety_checker.check(query)
    if safety_result.is_crisis:
        print(f"   ⚠️  CRISIS DETECTED: {safety_result.crisis_type}")
        print(f"   Response: {safety_result.response[:100]}...")
        return
    else:
        print("   ✓ No crisis detected")
    
    # 2. Preprocessing
    print("\n2. Preprocessing:")
    preprocessor = get_preprocessor()
    preprocessed = preprocessor.preprocess(query)
    print(f"   Language: {preprocessed.language}")
    print(f"   Translated: {preprocessed.was_translated}")
    print(f"   English text: {preprocessed.english_text}")
    
    # 3. Emotion classification
    print("\n3. Emotion Classification:")
    emotion_model = get_emotion_model()
    emotion_result = emotion_model.predict(preprocessed.english_text)
    print(f"   Emotion: {emotion_result['emotion']}")
    print(f"   Confidence: {emotion_result['confidence']:.2%}")
    print(f"   Top 3 emotions:")
    sorted_emotions = sorted(
        emotion_result['all_scores'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    for emotion, score in sorted_emotions:
        print(f"      {emotion}: {score:.2%}")
    
    # 4. Intent classification
    print("\n4. Intent Classification:")
    intent_model = get_intent_model()
    intent_result = intent_model.predict(preprocessed.english_text)
    print(f"   Intent: {intent_result['intent']}")
    print(f"   Confidence: {intent_result['confidence']:.2%}")
    print(f"   Top 3 intents:")
    sorted_intents = sorted(
        intent_result['all_scores'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    for intent, score in sorted_intents:
        print(f"      {intent}: {score:.2%}")
    
    print("\n" + "=" * 60)


def main():
    """Main interactive loop"""
    print("=" * 60)
    print("Mental Health Chatbot - Interactive Model Testing")
    print("=" * 60)
    print("\nThis script lets you test the models with your own queries.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Load models
    print("Loading models...")
    emotion_model = get_emotion_model()
    intent_model = get_intent_model()
    print(f"✓ Emotion model: {'ONNX' if emotion_model.is_loaded() else 'Rule-based'}")
    print(f"✓ Intent model: {'ONNX' if intent_model.is_loaded() else 'Rule-based'}")
    print()
    
    # Example queries
    print("Example queries to try:")
    print("  - I feel really sad and hopeless")
    print("  - I'm so anxious about my exam")
    print("  - I want to kill myself")
    print("  - I feel great today!")
    print("  - मुझे बहुत दुख हो रहा है (Hindi)")
    print()
    
    while True:
        try:
            query = input("Enter your query (or 'quit' to exit): ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            test_query(query)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
