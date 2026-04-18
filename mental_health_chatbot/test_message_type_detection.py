#!/usr/bin/env python3
"""
Test script for message type detection
Validates that short replies and contextual messages are handled correctly
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from pipeline.message_type import detect_message_type


def test_message_type_detection():
    """Test message type detection with various inputs"""
    
    print("🧪 MESSAGE TYPE DETECTION TESTS")
    print("=" * 60)
    
    test_cases = [
        # Short replies
        ("yes", False, "short_reply"),
        ("no", False, "short_reply"),
        ("okay", False, "short_reply"),
        ("maybe", False, "short_reply"),
        
        # Temporal/contextual references
        ("2 days earlier", False, "contextual"),
        ("just yesterday", False, "contextual"),
        ("about a week ago", True, "contextual"),
        ("since last month", True, "contextual"),
        
        # Emotional content (should still be detected)
        ("I feel sad", False, "emotional"),
        ("I'm really anxious and worried", False, "emotional"),
        ("I feel hopeless", False, "emotional"),
        ("sad", False, "emotional"),  # Short but emotional
        
        # Neutral conversational
        ("I see", False, "neutral"),
        ("I understand", False, "neutral"),
        ("got it", False, "short_reply"),
        ("makes sense", False, "neutral"),
        
        # Questions
        ("why?", True, "contextual"),
        ("what do you mean?", True, "contextual"),
        
        # Mixed (contextual with emotion)
        ("I've been feeling sad for 2 weeks", False, "emotional"),
        ("It started yesterday and I feel terrible", False, "emotional"),
        
        # Longer neutral
        ("I'm not sure what to say about that", False, "neutral"),
        ("Can you explain more about this", True, "contextual"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    print("\n📋 Test Cases:\n")
    
    for text, context_available, expected_type in test_cases:
        result = detect_message_type(text, context_available)
        actual_type = result['type']
        confidence = result['confidence']
        reason = result['reason']
        
        if actual_type == expected_type:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
        
        print(f"{status} | '{text}'")
        print(f"       Expected: {expected_type}")
        print(f"       Got: {actual_type} (confidence: {confidence:.2f})")
        print(f"       Reason: {reason}")
        print()
    
    print("=" * 60)
    print(f"📊 RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} tests failed")
    
    return passed == total


def test_edge_cases():
    """Test edge cases"""
    
    print("\n\n🔍 EDGE CASE TESTS")
    print("=" * 60)
    
    edge_cases = [
        # Very short emotional
        ("sad", False),
        ("angry", False),
        ("tired", False),
        
        # Numbers only
        ("3", False),
        ("2 days", False),
        
        # Punctuation only
        ("...", False),
        ("?", False),
        
        # Mixed language (should still work)
        ("yes yaar", False),
        ("okay thanks", False),
    ]
    
    print("\n📋 Edge Cases:\n")
    
    for text, context_available in edge_cases:
        result = detect_message_type(text, context_available)
        print(f"Input: '{text}'")
        print(f"  Type: {result['type']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Reason: {result['reason']}")
        print()


def test_context_dependency():
    """Test how context affects classification"""
    
    print("\n\n🔄 CONTEXT DEPENDENCY TESTS")
    print("=" * 60)
    
    test_inputs = [
        "2 days",
        "yesterday",
        "I think so",
        "not really",
        "maybe"
    ]
    
    print("\n📋 Same input with/without context:\n")
    
    for text in test_inputs:
        result_no_context = detect_message_type(text, context_available=False)
        result_with_context = detect_message_type(text, context_available=True)
        
        print(f"Input: '{text}'")
        print(f"  Without context: {result_no_context['type']} ({result_no_context['confidence']:.2f})")
        print(f"  With context: {result_with_context['type']} ({result_with_context['confidence']:.2f})")
        
        if result_no_context['type'] != result_with_context['type']:
            print(f"  ⚠️  Classification changed based on context")
        print()


def main():
    """Run all tests"""
    print("Starting Message Type Detection Test Suite...\n")
    
    # Run main tests
    all_passed = test_message_type_detection()
    
    # Run edge case tests
    test_edge_cases()
    
    # Run context dependency tests
    test_context_dependency()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ MESSAGE TYPE DETECTION IS WORKING CORRECTLY")
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW ABOVE")
    print("=" * 60)


if __name__ == "__main__":
    main()
