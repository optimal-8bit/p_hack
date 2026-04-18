#!/usr/bin/env python3
"""
Comprehensive test script for Advanced Response Engine (Phase 2)
Tests all new features and validates existing functionality
"""

import sys
import os
import asyncio
import time
from typing import List, Dict

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from pipeline.orchestrator import get_orchestrator
from response_engine.advanced_response_builder import get_advanced_response_builder
from response_engine.reflection import generate_reflection
from pipeline.context_tracker import get_context_tracker


class AdvancedResponseEngineTest:
    """Comprehensive test suite for advanced response engine"""
    
    def __init__(self):
        self.orchestrator = get_orchestrator()
        self.advanced_builder = get_advanced_response_builder()
        self.context_tracker = get_context_tracker()
        self.test_results = []
    
    async def run_all_tests(self):
        """Run all test scenarios"""
        print("🧠 ADVANCED RESPONSE ENGINE TEST SUITE")
        print("=" * 50)
        
        # Test 1: Confidence-aware emotion handling
        await self._test_confidence_aware_emotions()
        
        # Test 2: Reflection layer
        await self._test_reflection_layer()
        
        # Test 3: Professional help gating
        await self._test_professional_help_gating()
        
        # Test 4: Response variation and structure
        await self._test_response_variation()
        
        # Test 5: Context-aware trajectory analysis
        await self._test_trajectory_analysis()
        
        # Test 6: Short input handling
        await self._test_short_input_handling()
        
        # Test 7: Depth detection and intensity scaling
        await self._test_depth_detection()
        
        # Test 8: Multilingual fixes (Hinglish)
        await self._test_multilingual_fixes()
        
        # Test 9: No fake personalization
        await self._test_no_fake_personalization()
        
        # Test 10: Existing functionality preservation
        await self._test_existing_functionality()
        
        # Print summary
        self._print_test_summary()
    
    async def _test_confidence_aware_emotions(self):
        """Test emotion confidence handling"""
        print("\n🎯 Test 1: Confidence-Aware Emotion Handling")
        
        # Simulate low confidence emotion
        session_id = "test_confidence"
        self.context_tracker.clear_session(session_id)
        
        # Test with simulated low confidence (we'll mock this)
        response = await self.orchestrator.process_message(
            session_id, "I feel sad"
        )
        
        # Check if response handles uncertainty appropriately
        contains_uncertainty = any(phrase in response.response_text.lower() for phrase in [
            "may not be fully understanding",
            "it sounds like",
            "it seems like"
        ])
        
        self._record_test("Confidence-aware emotions", contains_uncertainty, 
                         f"Response: {response.response_text}")
    
    async def _test_reflection_layer(self):
        """Test reflection generation"""
        print("\n🪞 Test 2: Reflection Layer")
        
        test_cases = [
            ("I feel like I'm failing everything", "it feels like things aren't going the way you hoped"),
            ("I feel so alone", "it feels like you're disconnected from others"),
            ("I can't handle this anymore", "it feels like you've reached your limit"),
            ("I'm worried about my exams", "exams")  # Should capture "exams"
        ]
        
        all_passed = True
        for user_input, expected_pattern in test_cases:
            reflection = generate_reflection(user_input, "sadness")
            
            if reflection and expected_pattern.lower() in reflection.lower():
                print(f"  ✅ '{user_input}' → '{reflection}'")
            else:
                print(f"  ❌ '{user_input}' → '{reflection}' (expected: {expected_pattern})")
                all_passed = False
        
        self._record_test("Reflection layer", all_passed, "Pattern-based reflections")
    
    async def _test_professional_help_gating(self):
        """Test strict professional help gating"""
        print("\n🚪 Test 3: Professional Help Gating")
        
        session_id = "test_gating"
        self.context_tracker.clear_session(session_id)
        
        # Test early turns (should NOT suggest professional help)
        early_responses = []
        for i in range(3):
            response = await self.orchestrator.process_message(
                session_id, "I feel really depressed and hopeless"
            )
            early_responses.append(response.response_text)
        
        # Check no early suggestions
        early_suggestions = any("therapist" in resp.lower() or "counselor" in resp.lower() 
                               for resp in early_responses)
        
        # Test later turns with persistent negative emotion
        later_responses = []
        for i in range(3):
            response = await self.orchestrator.process_message(
                session_id, "I still feel hopeless and can't go on"
            )
            later_responses.append(response.response_text)
        
        # Check for appropriate later suggestion
        later_suggestions = any("therapist" in resp.lower() or "counselor" in resp.lower() 
                               for resp in later_responses)
        
        gating_works = not early_suggestions and later_suggestions
        
        self._record_test("Professional help gating", gating_works,
                         f"Early: {early_suggestions}, Later: {later_suggestions}")
    
    async def _test_response_variation(self):
        """Test response structure variation"""
        print("\n🔄 Test 4: Response Variation")
        
        session_id = "test_variation"
        self.context_tracker.clear_session(session_id)
        
        # Send same emotion/intent multiple times
        responses = []
        for i in range(5):
            response = await self.orchestrator.process_message(
                session_id, "I feel anxious about everything"
            )
            responses.append(response.response_text)
        
        # Check for variation (no identical responses)
        unique_responses = len(set(responses))
        variation_good = unique_responses >= 4  # At least 4 out of 5 should be different
        
        print(f"  Generated {unique_responses}/5 unique responses")
        for i, resp in enumerate(responses):
            print(f"  {i+1}: {resp[:80]}...")
        
        self._record_test("Response variation", variation_good,
                         f"{unique_responses}/5 unique responses")
    
    async def _test_trajectory_analysis(self):
        """Test emotional trajectory analysis"""
        print("\n📈 Test 5: Trajectory Analysis")
        
        session_id = "test_trajectory"
        self.context_tracker.clear_session(session_id)
        
        # Create persistent negative trajectory
        negative_inputs = [
            "I feel sad",
            "I'm still feeling down", 
            "Everything feels hopeless",
            "I can't see any point anymore"
        ]
        
        responses = []
        for msg in negative_inputs:
            response = await self.orchestrator.process_message(session_id, msg)
            responses.append(response.response_text)
        
        # Later responses should show escalated support
        later_response = responses[-1]
        escalated_support = any(phrase in later_response.lower() for phrase in [
            "really hard", "incredibly", "heavy", "overwhelming", 
            "breaking point", "lot of pain"
        ])
        
        self._record_test("Trajectory analysis", escalated_support,
                         f"Final response: {later_response[:100]}...")
    
    async def _test_short_input_handling(self):
        """Test short input mode"""
        print("\n📝 Test 6: Short Input Handling")
        
        session_id = "test_short"
        self.context_tracker.clear_session(session_id)
        
        short_inputs = ["tired", "sad", "angry", "stressed"]
        
        all_clarifying = True
        for short_input in short_inputs:
            response = await self.orchestrator.process_message(session_id, short_input)
            
            # Should ask clarifying questions
            is_clarifying = "?" in response.response_text and any(word in response.response_text.lower() 
                                                                for word in ["more", "tell", "what", "how"])
            
            print(f"  '{short_input}' → {response.response_text}")
            
            if not is_clarifying:
                all_clarifying = False
        
        self._record_test("Short input handling", all_clarifying, "Clarifying questions")
    
    async def _test_depth_detection(self):
        """Test depth detection and intensity scaling"""
        print("\n🎯 Test 7: Depth Detection")
        
        session_id = "test_depth"
        self.context_tracker.clear_session(session_id)
        
        # High intensity input
        high_intensity = "I can't go on, there's no point to anything, I'm completely broken"
        response = await self.orchestrator.process_message(session_id, high_intensity)
        
        # Should use deeper validation and avoid shallow coping
        deep_response = any(phrase in response.response_text.lower() for phrase in [
            "pain", "breaking point", "overwhelming", "heavy", "incredibly"
        ])
        
        # Should not have shallow coping like "try deep breathing"
        no_shallow = not any(phrase in response.response_text.lower() for phrase in [
            "deep breath", "try", "maybe", "could"
        ])
        
        depth_appropriate = deep_response and no_shallow
        
        self._record_test("Depth detection", depth_appropriate,
                         f"Response: {response.response_text}")
    
    async def _test_multilingual_fixes(self):
        """Test multilingual handling (Hinglish simulation)"""
        print("\n🌍 Test 8: Multilingual Fixes")
        
        session_id = "test_multilingual"
        self.context_tracker.clear_session(session_id)
        
        # Simulate mixed language input (should be processed as English)
        mixed_input = "I am feeling very sad yaar, kya karu"
        response = await self.orchestrator.process_message(session_id, mixed_input)
        
        # Should not break and should provide reasonable response
        no_errors = len(response.response_text) > 20 and "error" not in response.response_text.lower()
        
        self._record_test("Multilingual fixes", no_errors,
                         f"Handled mixed language input: {response.response_text[:50]}...")
    
    async def _test_no_fake_personalization(self):
        """Test that no fake context is injected"""
        print("\n🚫 Test 9: No Fake Personalization")
        
        session_id = "test_personalization"
        self.context_tracker.clear_session(session_id)
        
        # Send generic message without mentioning work/exams
        response = await self.orchestrator.process_message(
            session_id, "I feel overwhelmed with everything"
        )
        
        # Should NOT mention work, exams, or other fake context
        no_fake_context = not any(word in response.response_text.lower() 
                                 for word in ["work", "exam", "job", "school", "study"])
        
        self._record_test("No fake personalization", no_fake_context,
                         f"Response: {response.response_text}")
    
    async def _test_existing_functionality(self):
        """Test that existing functionality still works"""
        print("\n🔧 Test 10: Existing Functionality Preservation")
        
        session_id = "test_existing"
        self.context_tracker.clear_session(session_id)
        
        # Test crisis detection still works
        crisis_input = "I want to kill myself"
        response = await self.orchestrator.process_message(session_id, crisis_input)
        
        crisis_handled = response.is_crisis and "crisis" in response.response_text.lower()
        
        # Test normal emotion classification still works
        normal_input = "I feel happy today"
        response2 = await self.orchestrator.process_message(session_id, normal_input)
        
        emotion_works = response2.emotion in ["joy", "neutral"] and not response2.is_crisis
        
        existing_works = crisis_handled and emotion_works
        
        self._record_test("Existing functionality", existing_works,
                         f"Crisis: {crisis_handled}, Emotion: {emotion_works}")
    
    def _record_test(self, test_name: str, passed: bool, details: str):
        """Record test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if not passed or True:  # Show details for all tests
            print(f"    Details: {details}")
        
        self.test_results.append({
            "name": test_name,
            "passed": passed,
            "details": details
        })
    
    def _print_test_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("🧪 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result["passed"])
        total = len(self.test_results)
        
        print(f"Tests passed: {passed}/{total}")
        print(f"Success rate: {passed/total*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Advanced Response Engine is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Review the details above.")
            
            # Show failed tests
            failed_tests = [r for r in self.test_results if not r["passed"]]
            if failed_tests:
                print("\nFailed tests:")
                for test in failed_tests:
                    print(f"  - {test['name']}: {test['details']}")


async def main():
    """Run the test suite"""
    print("Starting Advanced Response Engine Test Suite...")
    print("This will test all Phase 2 enhancements.")
    
    tester = AdvancedResponseEngineTest()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())