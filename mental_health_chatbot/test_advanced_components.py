#!/usr/bin/env python3
"""
Test individual advanced response engine components
Tests components in isolation without requiring full pipeline
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from response_engine.reflection import generate_reflection
from response_engine.advanced_response_builder import (
    AdvancedResponseBuilder, 
    VariationEngine, 
    EmotionalTrajectoryAnalyzer,
    DepthDetector,
    ProfessionalHelpGating
)


def test_reflection_layer():
    """Test reflection generation"""
    print("🪞 Testing Reflection Layer")
    print("-" * 30)
    
    test_cases = [
        ("I feel like I'm failing everything", "it feels like things aren't going the way you hoped"),
        ("I feel so alone", "it feels like you're disconnected from others"),
        ("I can't handle this anymore", "it feels like you've reached your limit"),
        ("I'm worried about my exams", "exams"),
        ("I hate my job", "it seems like"),
        ("I'm not good enough", "it feels like you're doubting your worth"),
        ("There's no point to anything", "it feels like things have lost their meaning")
    ]
    
    passed = 0
    total = len(test_cases)
    
    for user_input, expected_pattern in test_cases:
        reflection = generate_reflection(user_input, "sadness")
        
        if reflection and expected_pattern.lower() in reflection.lower():
            print(f"  ✅ '{user_input}' → '{reflection}'")
            passed += 1
        else:
            print(f"  ❌ '{user_input}' → '{reflection}' (expected: {expected_pattern})")
    
    print(f"\nReflection Tests: {passed}/{total} passed")
    return passed == total


def test_variation_engine():
    """Test variation engine"""
    print("\n🔄 Testing Variation Engine")
    print("-" * 30)
    
    engine = VariationEngine()
    session_id = "test_session"
    
    # Test validation variations
    variations = []
    for i in range(5):
        variation = engine.get_varied_phrase(
            session_id, "validation", engine.VALIDATION_VARIANTS
        )
        variations.append(variation)
        print(f"  Variation {i+1}: {variation}")
    
    # Check for variety (should not repeat immediately)
    unique_count = len(set(variations))
    variety_good = unique_count >= 3  # At least 3 different out of 5
    
    print(f"\nVariation Tests: {unique_count}/5 unique phrases")
    return variety_good


def test_trajectory_analyzer():
    """Test emotional trajectory analysis"""
    print("\n📈 Testing Trajectory Analyzer")
    print("-" * 30)
    
    analyzer = EmotionalTrajectoryAnalyzer()
    
    test_cases = [
        (["sadness", "sadness", "sadness"], "persistent_distress"),
        (["sadness", "fear", "anger"], "fluctuating"),
        (["joy", "joy"], "normal"),
        ([], "initial")
    ]
    
    passed = 0
    total = len(test_cases)
    
    for emotions, expected_state in test_cases:
        result = analyzer.analyze_trajectory(emotions)
        
        if result["state"] == expected_state:
            print(f"  ✅ {emotions} → {result['state']} (intensity: {result['intensity']})")
            passed += 1
        else:
            print(f"  ❌ {emotions} → {result['state']} (expected: {expected_state})")
    
    print(f"\nTrajectory Tests: {passed}/{total} passed")
    return passed == total


def test_depth_detector():
    """Test depth detection"""
    print("\n🎯 Testing Depth Detector")
    print("-" * 30)
    
    detector = DepthDetector()
    
    test_cases = [
        ("I can't go on, there's no point", "high"),
        ("I feel hopeless and worthless", "high"),
        ("I can't handle this anymore", "moderate"),
        ("I feel sad today", "normal"),
        ("I'm a bit worried", "normal")
    ]
    
    passed = 0
    total = len(test_cases)
    
    for text, expected_intensity in test_cases:
        intensity = detector.detect_intensity(text)
        
        if intensity == expected_intensity:
            print(f"  ✅ '{text}' → {intensity}")
            passed += 1
        else:
            print(f"  ❌ '{text}' → {intensity} (expected: {expected_intensity})")
    
    print(f"\nDepth Tests: {passed}/{total} passed")
    return passed == total


def test_professional_help_gating():
    """Test professional help gating logic"""
    print("\n🚪 Testing Professional Help Gating")
    print("-" * 30)
    
    gating = ProfessionalHelpGating()
    
    test_cases = [
        # (turn_number, trajectory_state, negative_count, intensity, text_length, last_suggestion, expected)
        (2, {"state": "persistent_distress", "negative_count": 3, "intensity": "high"}, 50, None, False),  # Too early
        (5, {"state": "normal", "negative_count": 1, "intensity": "low"}, 50, None, False),  # Not persistent
        (5, {"state": "persistent_distress", "negative_count": 3, "intensity": "high"}, 50, None, True),   # Should suggest
        (6, {"state": "persistent_distress", "negative_count": 3, "intensity": "high"}, 15, None, False),  # Too short
        (7, {"state": "persistent_distress", "negative_count": 3, "intensity": "high"}, 50, 6, False),    # Too recent
    ]
    
    passed = 0
    total = len(test_cases)
    
    for turn_num, trajectory, text_len, last_sugg, expected in test_cases:
        should_suggest = gating.should_suggest_professional_help(
            turn_number=turn_num,
            trajectory=trajectory,
            text_length=text_len,
            last_suggestion_turn=last_sugg
        )
        
        if should_suggest == expected:
            print(f"  ✅ Turn {turn_num}, {trajectory['state']}, len={text_len} → {should_suggest}")
            passed += 1
        else:
            print(f"  ❌ Turn {turn_num}, {trajectory['state']}, len={text_len} → {should_suggest} (expected: {expected})")
    
    print(f"\nGating Tests: {passed}/{total} passed")
    return passed == total


def test_advanced_response_builder():
    """Test advanced response builder integration"""
    print("\n🧠 Testing Advanced Response Builder")
    print("-" * 30)
    
    builder = AdvancedResponseBuilder()
    
    # Test basic response building
    response1 = builder.build_response(
        user_text="I feel like I'm failing everything",
        emotion="sadness",
        emotion_confidence=0.9,
        intent="sadness and depression",
        turn_number=1,
        session_id="test_session",
        context_emotions=[],
        base_template=""
    )
    
    print(f"  Response 1: {response1}")
    
    # Test low confidence emotion
    response2 = builder.build_response(
        user_text="I feel bad",
        emotion="sadness",
        emotion_confidence=0.5,  # Low confidence
        intent="general emotional support",
        turn_number=2,
        session_id="test_session",
        context_emotions=["sadness"],
        base_template=""
    )
    
    print(f"  Response 2 (low confidence): {response2}")
    
    # Test short input
    response3 = builder.build_response(
        user_text="tired",
        emotion="neutral",
        emotion_confidence=0.8,
        intent="general emotional support",
        turn_number=3,
        session_id="test_session",
        context_emotions=["sadness", "neutral"],
        base_template=""
    )
    
    print(f"  Response 3 (short): {response3}")
    
    # Check basic requirements
    has_responses = all(len(r) > 20 for r in [response1, response2, response3])
    has_uncertainty = "may not be fully understanding" in response2.lower()
    has_question = "?" in response3
    
    builder_works = has_responses and has_uncertainty and has_question
    
    print(f"\nBuilder Tests: {'✅ PASS' if builder_works else '❌ FAIL'}")
    print(f"  Has responses: {has_responses}")
    print(f"  Has uncertainty handling: {has_uncertainty}")
    print(f"  Has clarifying question: {has_question}")
    
    return builder_works


def main():
    """Run all component tests"""
    print("🧪 ADVANCED RESPONSE ENGINE COMPONENT TESTS")
    print("=" * 50)
    
    tests = [
        test_reflection_layer,
        test_variation_engine,
        test_trajectory_analyzer,
        test_depth_detector,
        test_professional_help_gating,
        test_advanced_response_builder
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("🧪 COMPONENT TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL COMPONENT TESTS PASSED!")
        print("Advanced Response Engine components are working correctly.")
    else:
        print("\n⚠️  Some component tests failed.")
        print("Review the details above for specific issues.")


if __name__ == "__main__":
    main()