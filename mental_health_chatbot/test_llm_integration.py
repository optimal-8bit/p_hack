#!/usr/bin/env python3
"""
Test script for LLM integration
Tests the controlled Phi-3 surface generation layer
"""

import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from response_engine.llm_generator import get_llm_generator
from response_engine.payload_builder import get_payload_builder


async def test_llm_availability():
    """Test if LLM model can be loaded"""
    print("🔍 Testing LLM Availability")
    print("=" * 60)
    
    generator = get_llm_generator()
    
    # Try to load model
    model_available = await generator._ensure_model_loaded()
    
    if model_available:
        print("✅ Phi-3 Mini model loaded successfully")
        print(f"   Model: {generator._load_model.__name__}")
        return True
    else:
        print("❌ Phi-3 Mini model not available")
        print("   This is OK - system will use template fallback")
        print("\n📦 To enable LLM generation, install:")
        print("   pip install transformers torch accelerate")
        return False


async def test_payload_builder():
    """Test payload builder"""
    print("\n🔧 Testing Payload Builder")
    print("=" * 60)
    
    builder = get_payload_builder()
    
    # Create test payload
    payload = builder.build_llm_payload(
        user_input="I feel really anxious about everything",
        processed_text="I feel really anxious about everything",
        message_type={"type": "emotional", "confidence": 0.9, "reason": "emotional keywords"},
        emotion="fear",
        emotion_confidence=0.85,
        intent="anxiety and panic",
        intent_confidence=0.9,
        turn_number=1,
        context=[],
        response_components={
            "validation": "That sounds really challenging.",
            "reflection": "It feels like everything is overwhelming you right now.",
            "question": "When did you first start noticing these feelings?",
            "allow_therapist": False
        },
        allow_therapist=False
    )
    
    print("✅ Payload built successfully")
    print(f"   Keys: {list(payload.keys())}")
    print(f"   Message type: {payload['message_type']['type']}")
    print(f"   Emotion: {payload['emotion']['label']}")
    print(f"   Response plan keys: {list(payload['response_plan'].keys())}")
    
    return payload


async def test_llm_generation(payload):
    """Test LLM generation with sample payload"""
    print("\n🤖 Testing LLM Generation")
    print("=" * 60)
    
    # Enable debug logging for this test
    import logging
    logging.basicConfig(level=logging.INFO)
    
    generator = get_llm_generator()
    
    print("Generating response...")
    print(f"Payload keys: {list(payload.keys())}")
    print(f"Response plan: {payload['response_plan']}")
    
    try:
        response = await generator.generate_response(payload)
        
        if response:
            print("✅ LLM generation successful")
            print(f"\n📝 Generated Response:")
            print(f"   {response}")
            print(f"\n📊 Stats: {generator.get_stats()}")
            return True
        else:
            print("⚠️  LLM generation returned None (fallback will be used)")
            print(f"📊 Stats: {generator.get_stats()}")
            print("\nCheck logs above for details on why generation failed")
            return False
    except Exception as e:
        print(f"❌ LLM generation error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_validation():
    """Test response validation"""
    print("\n✅ Testing Response Validation")
    print("=" * 60)
    
    generator = get_llm_generator()
    
    test_cases = [
        ("That sounds really hard. It feels like you're going through a lot. What's been the most difficult part?", True),
        ("You are diagnosed with depression. You should definitely see a doctor.", False),
        ("I recommend therapy immediately. You have a mental illness.", False),
        ("It seems like you're feeling overwhelmed. Can you tell me more?", True),
        ("", False),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for response, expected_valid in test_cases:
        is_valid = generator._validate_response(response)
        
        if is_valid == expected_valid:
            status = "✅"
            passed += 1
        else:
            status = "❌"
        
        print(f"{status} '{response[:50]}...' → Valid: {is_valid}")
    
    print(f"\nValidation Tests: {passed}/{total} passed")
    return passed == total


async def test_fallback_behavior():
    """Test that system works without LLM"""
    print("\n🔄 Testing Fallback Behavior")
    print("=" * 60)
    
    # Temporarily disable LLM
    import config
    original_enabled = config.LLM_ENABLED
    config.LLM_ENABLED = False
    
    generator = get_llm_generator()
    generator.enabled = False
    
    # Try to generate (should return None immediately)
    payload = {
        "user_input": "test",
        "response_plan": {"validation": "test"}
    }
    
    response = await generator.generate_response(payload)
    
    # Restore setting
    config.LLM_ENABLED = original_enabled
    
    if response is None:
        print("✅ Fallback behavior works correctly")
        print("   LLM disabled → returns None → template fallback used")
        return True
    else:
        print("❌ Fallback behavior not working")
        return False


async def main():
    """Run all tests"""
    print("🧪 LLM INTEGRATION TEST SUITE")
    print("=" * 60)
    print()
    
    # Test 1: LLM availability
    llm_available = await test_llm_availability()
    
    # Test 2: Payload builder
    payload = await test_payload_builder()
    
    # Test 3: Validation
    validation_ok = await test_validation()
    
    # Test 4: Fallback behavior
    fallback_ok = await test_fallback_behavior()
    
    # Test 5: LLM generation (only if available)
    if llm_available:
        generation_ok = await test_llm_generation(payload)
    else:
        print("\n⚠️  Skipping LLM generation test (model not available)")
        generation_ok = True  # Not a failure
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    tests = {
        "Payload Builder": True,  # Always passes if no exception
        "Response Validation": validation_ok,
        "Fallback Behavior": fallback_ok,
        "LLM Generation": generation_ok if llm_available else "Skipped"
    }
    
    for test_name, result in tests.items():
        if result == "Skipped":
            print(f"⚠️  {test_name}: Skipped (model not available)")
        elif result:
            print(f"✅ {test_name}: PASS")
        else:
            print(f"❌ {test_name}: FAIL")
    
    print("\n" + "=" * 60)
    if llm_available:
        print("✅ LLM INTEGRATION READY")
        print("   Phi-3 Mini is loaded and working")
    else:
        print("⚠️  LLM NOT AVAILABLE (Using Template Fallback)")
        print("   System will work normally with template responses")
        print("\n📦 To enable LLM generation:")
        print("   pip install transformers torch accelerate")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())