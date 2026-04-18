#!/usr/bin/env python3
"""
Simple integration test for message type detection in orchestrator
Tests without requiring full ML models
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from pipeline.message_type import detect_message_type
from pipeline.context_tracker import get_context_tracker


def test_message_type_integration():
    """Test message type detection integration"""
    
    print("🔗 MESSAGE TYPE INTEGRATION TEST")
    print("=" * 50)
    
    # Test the detect_message_type function
    test_cases = [
        ("yes", False, "short_reply"),
        ("just yesterday", False, "contextual"),
        ("got it", False, "short_reply"),
        ("I'm not sure what to say about that", False, "neutral"),
        ("I feel sad", False, "emotional"),
    ]
    
    print("\n📋 Testing Updated Detection:\n")
    
    passed = 0
    total = len(test_cases)
    
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
    
    print("=" * 50)
    print(f"📊 RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    return passed == total


def test_context_tracker_integration():
    """Test context tracker integration"""
    
    print("\n🔄 CONTEXT TRACKER INTEGRATION TEST")
    print("=" * 50)
    
    tracker = get_context_tracker()
    session_id = "test_integration"
    
    # Clear session
    tracker.clear_session(session_id)
    
    # Test new methods
    last_language = tracker.get_last_language(session_id)
    last_intent = tracker.get_last_intent(session_id)
    
    print(f"✅ get_last_language() works: {last_language}")
    print(f"✅ get_last_intent() works: {last_intent}")
    
    return True


def main():
    """Run integration tests"""
    print("Starting Message Type Integration Tests...\n")
    
    # Test message type detection
    detection_passed = test_message_type_integration()
    
    # Test context tracker integration
    context_passed = test_context_tracker_integration()
    
    print("\n" + "=" * 50)
    if detection_passed and context_passed:
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("✅ Message type detection is working correctly")
        print("✅ Context tracker integration is working")
        print("\n🚀 Ready for full pipeline testing!")
    else:
        print("⚠️  Some integration tests failed")
        if not detection_passed:
            print("❌ Message type detection issues")
        if not context_passed:
            print("❌ Context tracker integration issues")
    print("=" * 50)


if __name__ == "__main__":
    main()