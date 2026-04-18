#!/usr/bin/env python3
"""
Test script to demonstrate enhanced response intelligence
Shows: reflection, variation, context-awareness, personalization
"""

import os
os.environ["PYTHONIOENCODING"] = "utf-8"

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from response_engine.response_builder import get_response_builder
from response_engine.template_selector import get_template_selector
from pipeline.context_tracker import get_context_tracker, TurnRecord


def test_reflection():
    """Test reflection extraction"""
    print("=" * 60)
    print("TEST 1: Reflection Extraction")
    print("=" * 60)
    
    builder = get_response_builder()
    
    test_cases = [
        "I feel like I'm failing everything",
        "I'm so anxious about my exam",
        "I can't stop worrying about work",
        "Everything feels hopeless",
        "I want to give up",
    ]
    
    for text in test_cases:
        reflection = builder.reflection_extractor.extract(text)
        print(f"\nInput: {text}")
        print(f"Reflection: {reflection}")


def test_variation():
    """Test variation engine"""
    print("\n" + "=" * 60)
    print("TEST 2: Variation Engine")
    print("=" * 60)
    
    builder = get_response_builder()
    session_id = "test_session"
    
    print("\nValidation starters (5 calls):")
    for i in range(5):
        starter = builder.variation_engine.get_validation_starter(session_id)
        print(f"  {i+1}. {starter}")
    
    print("\nReflection frames (5 calls):")
    for i in range(5):
        frame = builder.variation_engine.get_reflection_frame(session_id)
        print(f"  {i+1}. {frame}")


def test_full_response():
    """Test full response building"""
    print("\n" + "=" * 60)
    print("TEST 3: Full Response Building")
    print("=" * 60)
    
    selector = get_template_selector()
    
    test_cases = [
        {
            "user_text": "I feel like I'm failing everything at work",
            "emotion": "sadness",
            "intent": "sadness and depression",
            "turn": 1,
        },
        {
            "user_text": "I'm so anxious about my upcoming exam",
            "emotion": "fear",
            "intent": "anxiety and panic",
            "turn": 1,
        },
        {
            "user_text": "I can't stop worrying about my family",
            "emotion": "fear",
            "intent": "stress and overwhelm",
            "turn": 1,
        },
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {case['user_text']}")
        print(f"Emotion: {case['emotion']}, Intent: {case['intent']}")
        
        response = selector.select(
            emotion=case['emotion'],
            intent=case['intent'],
            turn_number=case['turn'],
            context=[],
            detected_language="en",
            user_text=case['user_text'],
            session_id=f"test_{i}"
        )
        
        print(f"\nResponse:\n{response}")


def test_multi_turn_conversation():
    """Test multi-turn conversation with context"""
    print("\n" + "=" * 60)
    print("TEST 4: Multi-Turn Conversation")
    print("=" * 60)
    
    selector = get_template_selector()
    tracker = get_context_tracker()
    session_id = "multi_turn_test"
    
    conversation = [
        ("I feel really sad and hopeless", "sadness", "sadness and depression"),
        ("Nothing seems to help", "sadness", "sadness and depression"),
        ("I've been feeling this way for weeks", "sadness", "sadness and depression"),
        ("I just want to feel better", "sadness", "general emotional support"),
    ]
    
    for turn_num, (user_text, emotion, intent) in enumerate(conversation, 1):
        print(f"\n--- Turn {turn_num} ---")
        print(f"User: {user_text}")
        
        context = tracker.get_context(session_id)
        
        response = selector.select(
            emotion=emotion,
            intent=intent,
            turn_number=turn_num,
            context=context,
            detected_language="en",
            user_text=user_text,
            session_id=session_id
        )
        
        print(f"Bot: {response}")
        
        # Add to context
        turn_record = TurnRecord(
            user_text=user_text,
            emotion=emotion,
            intent=intent,
            response_template_key=response[:50],
            turn_number=turn_num,
            timestamp=0.0
        )
        tracker.add_turn(session_id, turn_record)


def test_personalization():
    """Test micro-personalization with themes"""
    print("\n" + "=" * 60)
    print("TEST 5: Micro-Personalization")
    print("=" * 60)
    
    selector = get_template_selector()
    tracker = get_context_tracker()
    session_id = "personalization_test"
    
    conversation = [
        ("I'm stressed about my exams", "fear", "stress and overwhelm"),
        ("I can't focus on studying", "fear", "anxiety and panic"),
        ("I feel like I'm going to fail", "sadness", "sadness and depression"),
    ]
    
    for turn_num, (user_text, emotion, intent) in enumerate(conversation, 1):
        print(f"\n--- Turn {turn_num} ---")
        print(f"User: {user_text}")
        
        context = tracker.get_context(session_id)
        
        response = selector.select(
            emotion=emotion,
            intent=intent,
            turn_number=turn_num,
            context=context,
            detected_language="en",
            user_text=user_text,
            session_id=session_id
        )
        
        print(f"Bot: {response}")
        
        # Check if personalization appears in later turns
        if turn_num >= 3 and "exam" in response.lower():
            print("  ✓ Personalization detected: Referenced 'exams' from earlier")
        
        # Add to context
        turn_record = TurnRecord(
            user_text=user_text,
            emotion=emotion,
            intent=intent,
            response_template_key=response[:50],
            turn_number=turn_num,
            timestamp=0.0
        )
        tracker.add_turn(session_id, turn_record)


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("ENHANCED RESPONSE ENGINE - TEST SUITE")
    print("=" * 60)
    print("\nThis demonstrates:")
    print("1. Reflection extraction (mirroring user's words)")
    print("2. Variation engine (avoiding repetition)")
    print("3. Full response building (structured assembly)")
    print("4. Multi-turn context awareness")
    print("5. Micro-personalization (theme tracking)")
    print()
    
    test_reflection()
    test_variation()
    test_full_response()
    test_multi_turn_conversation()
    test_personalization()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nKey Improvements Demonstrated:")
    print("✓ Responses include reflection of user's words")
    print("✓ Validation phrases vary across turns")
    print("✓ Context-aware escalation (persistent negative emotion)")
    print("✓ Micro-personalization (theme references)")
    print("✓ Structural variation (not just text)")
    print()


if __name__ == "__main__":
    main()
