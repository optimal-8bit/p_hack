#!/usr/bin/env python3
"""
Integration test for emotion hallucination fix
Tests the complete pipeline with message type detection
"""

import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from pipeline.orchestrator import get_orchestrator
from pipeline.context_tracker import get_context_tracker
from pipeline.message_type import detect_message_type


class EmotionHallucinationTest:
    """Test suite for emotion hallucination fix"""
    
    def __init__(self):
        self.orchestrator = get_orchestrator()
        self.context_tracker = get_context_tracker()
        self.test_results = []
    
    async def run_all_tests(self):
        """Run all test scenarios"""
        print("🧠 EMOTION HALLUCINATION FIX TEST SUITE")
        print("=" * 60)
        
        # Test 1: Short replies don't hallucinate emotions
        await self._test_short_replies()
        
        # Test 2: Contextual follow-ups use previous context
        await self._test_contextual_followups()
        
        # Test 3: Neutral inputs get appropriate responses
        await self._test_neutral_inputs()
        
        # Test 4: Emotional inputs still work normally
        await self._test_emotional_inputs()
        
        # Test 5: Language consistency for short replies
        await self._test_language_consistency()
        
        # Test 6: Context continuity
        await self._test_context_continuity()
        
        # Print summary
        self._print_test_summary()
    
    async def _test_short_replies(self):
        """Test that short replies don't hallucinate strong emotions"""
        print("\n🔍 Test 1: Short Replies (No Emotion Hallucination)")
        print("-" * 50)
        
        session_id = "test_short_replies"
        self.context_tracker.clear_session(session_id)
        
        # First establish some emotional context
        await self.orchestrator.process_message(session_id, "I feel really sad and anxious")
        
        # Now test short replies
        short_replies = ["yes", "no", "okay", "maybe", "2 days", "yesterday"]
        
        all_appropriate = True
        
        for reply in short_replies:
            response = await self.orchestrator.process_message(session_id, reply)
            
            # Check that response doesn't strongly validate non-existent emotions
            inappropriate_validations = [
                "that sounds really hard",
                "i can hear how much pain",
                "that must be incredibly difficult",
                "i sense how heavy this feels"
            ]
            
            has_inappropriate = any(phrase in response.response_text.lower() 
                                  for phrase in inappropriate_validations)
            
            # Check that it asks clarifying questions instead
            has_clarification = "?" in response.response_text and any(word in response.response_text.lower() 
                                                                    for word in ["more", "tell", "what", "how", "can you"])
            
            appropriate = not has_inappropriate and has_clarification
            
            if appropriate:
                print(f"  ✅ '{reply}' → Appropriate response")
                print(f"      Response: {response.response_text[:80]}...")
            else:
                print(f"  ❌ '{reply}' → Inappropriate response")
                print(f"      Response: {response.response_text[:80]}...")
                all_appropriate = False
        
        self._record_test("Short replies don't hallucinate emotions", all_appropriate,
                         f"Tested {len(short_replies)} short replies")
    
    async def _test_contextual_followups(self):
        """Test contextual follow-ups use previous context appropriately"""
        print("\n🔄 Test 2: Contextual Follow-ups")
        print("-" * 50)
        
        session_id = "test_contextual"
        self.context_tracker.clear_session(session_id)
        
        # Establish emotional context
        response1 = await self.orchestrator.process_message(
            session_id, "I've been feeling depressed for weeks"
        )
        
        # Test contextual follow-up
        response2 = await self.orchestrator.process_message(
            session_id, "since my job interview failed"
        )
        
        # Should acknowledge the context and continue appropriately
        contextual_appropriate = (
            "since" in response2.response_text.lower() or
            "job" in response2.response_text.lower() or
            "interview" in response2.response_text.lower() or
            any(phrase in response2.response_text.lower() for phrase in [
                "that makes sense", "i see", "i understand", "thank you for clarifying"
            ])
        )
        
        print(f"  Context response: {response2.response_text}")
        
        self._record_test("Contextual follow-ups handled appropriately", contextual_appropriate,
                         f"Response: {response2.response_text[:100]}...")
    
    async def _test_neutral_inputs(self):
        """Test neutral inputs get gentle exploration"""
        print("\n😐 Test 3: Neutral Inputs")
        print("-" * 50)
        
        session_id = "test_neutral"
        self.context_tracker.clear_session(session_id)
        
        neutral_inputs = [
            "I'm not sure what to say",
            "I don't know",
            "Can you help me",
            "What should I talk about"
        ]
        
        all_gentle = True
        
        for neutral_input in neutral_inputs:
            response = await self.orchestrator.process_message(session_id, neutral_input)
            
            # Should be gentle and exploratory, not assume strong emotions
            gentle_phrases = [
                "i'm here to listen", "what's on your mind", "how have you been feeling",
                "i'm here for you", "what would be helpful", "how can i help"
            ]
            
            is_gentle = any(phrase in response.response_text.lower() for phrase in gentle_phrases)
            
            # Should not assume strong emotions
            strong_assumptions = [
                "that sounds really hard", "i can hear your pain", "that must be difficult"
            ]
            
            has_assumptions = any(phrase in response.response_text.lower() for phrase in strong_assumptions)
            
            appropriate = is_gentle and not has_assumptions
            
            if appropriate:
                print(f"  ✅ '{neutral_input}' → Gentle exploration")
            else:
                print(f"  ❌ '{neutral_input}' → Inappropriate assumptions")
                all_gentle = False
            
            print(f"      Response: {response.response_text[:80]}...")
        
        self._record_test("Neutral inputs get gentle exploration", all_gentle,
                         f"Tested {len(neutral_inputs)} neutral inputs")
    
    async def _test_emotional_inputs(self):
        """Test that genuinely emotional inputs still work normally"""
        print("\n😢 Test 4: Emotional Inputs (Normal Processing)")
        print("-" * 50)
        
        session_id = "test_emotional"
        self.context_tracker.clear_session(session_id)
        
        emotional_inputs = [
            "I feel really sad and hopeless",
            "I'm so anxious I can't sleep",
            "I hate myself and everything",
            "I feel alone and scared"
        ]
        
        all_appropriate = True
        
        for emotional_input in emotional_inputs:
            response = await self.orchestrator.process_message(session_id, emotional_input)
            
            # Should validate emotions appropriately
            validation_phrases = [
                "that sounds", "i can hear", "i sense", "that must be", "i understand"
            ]
            
            has_validation = any(phrase in response.response_text.lower() for phrase in validation_phrases)
            
            # Should have empathetic tone
            empathetic_words = [
                "hard", "difficult", "tough", "challenging", "pain", "heavy"
            ]
            
            has_empathy = any(word in response.response_text.lower() for word in empathetic_words)
            
            appropriate = has_validation or has_empathy
            
            if appropriate:
                print(f"  ✅ Emotional input processed appropriately")
            else:
                print(f"  ❌ Emotional input not handled well")
                all_appropriate = False
            
            print(f"      Input: {emotional_input}")
            print(f"      Response: {response.response_text[:80]}...")
        
        self._record_test("Emotional inputs processed normally", all_appropriate,
                         f"Tested {len(emotional_inputs)} emotional inputs")
    
    async def _test_language_consistency(self):
        """Test language consistency for short replies"""
        print("\n🌍 Test 5: Language Consistency")
        print("-" * 50)
        
        session_id = "test_language"
        self.context_tracker.clear_session(session_id)
        
        # This test would require actual translation models
        # For now, just verify the logic doesn't break
        
        response1 = await self.orchestrator.process_message(session_id, "I feel sad")
        response2 = await self.orchestrator.process_message(session_id, "yes")
        
        # Both should be in same language (English in this case)
        language_consistent = (
            response1.detected_language == response2.detected_language == "en"
        )
        
        print(f"  Response 1 language: {response1.detected_language}")
        print(f"  Response 2 language: {response2.detected_language}")
        
        self._record_test("Language consistency maintained", language_consistent,
                         f"Both responses in {response1.detected_language}")
    
    async def _test_context_continuity(self):
        """Test that context continuity is maintained"""
        print("\n🔗 Test 6: Context Continuity")
        print("-" * 50)
        
        session_id = "test_continuity"
        self.context_tracker.clear_session(session_id)
        
        # Build conversation context
        await self.orchestrator.process_message(session_id, "I'm struggling with anxiety")
        await self.orchestrator.process_message(session_id, "It's been going on for months")
        
        # Short reply should maintain context
        response = await self.orchestrator.process_message(session_id, "yes")
        
        # Should reference the ongoing conversation appropriately
        context_maintained = any(phrase in response.response_text.lower() for phrase in [
            "anxiety", "months", "struggling", "been affecting", "going on"
        ]) or "?" in response.response_text
        
        print(f"  Context response: {response.response_text}")
        
        self._record_test("Context continuity maintained", context_maintained,
                         f"Response: {response.response_text[:100]}...")
    
    def _record_test(self, test_name: str, passed: bool, details: str):
        """Record test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"\n  {status}: {test_name}")
        print(f"    Details: {details}")
        
        self.test_results.append({
            "name": test_name,
            "passed": passed,
            "details": details
        })
    
    def _print_test_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🧪 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["passed"])
        total = len(self.test_results)
        
        print(f"Tests passed: {passed}/{total}")
        print(f"Success rate: {passed/total*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Emotion hallucination fix is working correctly")
            print("✅ Short replies handled appropriately")
            print("✅ Contextual messages use previous context")
            print("✅ Neutral inputs get gentle exploration")
            print("✅ Emotional inputs still work normally")
        else:
            print("\n⚠️  Some tests failed. Review the details above.")
            
            # Show failed tests
            failed_tests = [r for r in self.test_results if not r["passed"]]
            if failed_tests:
                print("\nFailed tests:")
                for test in failed_tests:
                    print(f"  - {test['name']}: {test['details']}")


async def test_message_type_detection_only():
    """Test just the message type detection component"""
    print("🔍 MESSAGE TYPE DETECTION COMPONENT TEST")
    print("=" * 60)
    
    test_cases = [
        ("yes", False, "short_reply"),
        ("2 days earlier", False, "contextual"),
        ("I feel sad", False, "emotional"),
        ("I don't know", False, "neutral"),
        ("okay thanks", False, "short_reply"),
        ("since yesterday", True, "contextual"),
        ("I'm really anxious and worried", False, "emotional"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for text, context_available, expected_type in test_cases:
        result = detect_message_type(text, context_available)
        actual_type = result['type']
        
        if actual_type == expected_type:
            print(f"✅ '{text}' → {actual_type}")
            passed += 1
        else:
            print(f"❌ '{text}' → {actual_type} (expected: {expected_type})")
    
    print(f"\nMessage Type Detection: {passed}/{total} passed ({passed/total*100:.1f}%)")
    return passed == total


async def main():
    """Run the test suite"""
    print("Starting Emotion Hallucination Fix Test Suite...")
    print("This tests the complete pipeline with message type detection.\n")
    
    # Test message type detection component first
    component_passed = await test_message_type_detection_only()
    
    if component_passed:
        print("\n✅ Message type detection component working correctly")
        print("Proceeding with integration tests...\n")
        
        # Run full integration tests
        tester = EmotionHallucinationTest()
        await tester.run_all_tests()
    else:
        print("\n❌ Message type detection component has issues")
        print("Fix component issues before running integration tests")


if __name__ == "__main__":
    asyncio.run(main())