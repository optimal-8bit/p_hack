#!/usr/bin/env python3
"""
Test Gemini API integration
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Load .env file from parent directory
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from response_engine.gemini_generator import get_gemini_generator


async def test_gemini():
    print("=" * 80)
    print("🧪 GEMINI API INTEGRATION TEST")
    print("=" * 80)
    
    generator = get_gemini_generator()
    
    # Check if API key is set
    if not generator.enabled:
        print("\n❌ GEMINI_API_KEY not set in environment")
        print("\n💡 To enable Gemini:")
        print("   1. Get API key from: https://makersuite.google.com/app/apikey")
        print("   2. Set environment variable:")
        print("      export GEMINI_API_KEY='your_key_here'  # Linux/Mac")
        print("      setx GEMINI_API_KEY 'your_key_here'    # Windows")
        print("   3. Or create .env file with GEMINI_API_KEY=your_key_here")
        print("\n✅ System will use template fallback (works perfectly without Gemini)")
        return
    
    print(f"\n✅ Gemini API key detected")
    print(f"⏱️  Timeout: {generator.timeout_seconds}s")
    
    # Test payload
    test_payload = {
        "user_input": "I feel anxious about everything",
        "processed_text": "i feel anxious about everything",
        "message_type": "emotional",
        "emotion": "fear",
        "emotion_confidence": 0.89,
        "intent": "anxiety and panic",
        "intent_confidence": 0.92,
        "context": {
            "turn_number": 1,
            "previous_emotions": [],
            "conversation_summary": "User expressing anxiety"
        },
        "decision_engine": {
            "should_validate": True,
            "should_reflect": True,
            "should_ask_question": True
        },
        "response_plan": {
            "validation": "That sounds really challenging.",
            "reflection": "It feels like the anxiety is affecting many areas of your life.",
            "question": "What situations tend to trigger these feelings the most?"
        },
        "constraints": {
            "max_sentences": 4,
            "no_diagnosis": True,
            "allow_therapist": False
        }
    }
    
    print("\n📦 Test Payload:")
    print(f"   Emotion: {test_payload['emotion']} ({test_payload['emotion_confidence']:.2f})")
    print(f"   Intent: {test_payload['intent']}")
    print(f"   Response Plan: {test_payload['response_plan']}")
    
    print("\n🚀 Generating response with Gemini...")
    
    try:
        response = await generator.generate_response(test_payload)
        
        if response:
            print(f"\n✅ SUCCESS!")
            print(f"\n📝 Generated Response:")
            print(f"   {response}")
            
            # Validate
            print(f"\n🔍 Validation:")
            print(f"   Length: {len(response.split())} words")
            print(f"   Contains validation: {'✅' if 'challenging' in response.lower() else '❌'}")
            print(f"   Contains reflection: {'✅' if 'anxiety' in response.lower() or 'feel' in response.lower() else '❌'}")
            print(f"   Contains question: {'✅' if '?' in response else '❌'}")
            
        else:
            print(f"\n⚠️  Gemini returned None (using fallback)")
            print(f"   This is normal - fallback system will use templates")
        
        # Show stats
        stats = generator.get_stats()
        print(f"\n📊 Statistics:")
        print(f"   Total attempts: {stats['total_attempts']}")
        print(f"   Successful: {stats['successful_generations']}")
        print(f"   Fallbacks: {stats['fallbacks']}")
        print(f"   Success rate: {stats['success_rate']}")
        if stats['successful_generations'] > 0:
            print(f"   Avg latency: {stats['avg_latency_ms']}ms")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ Test complete!")
    print("=" * 80)


async def test_multiple_requests():
    """Test multiple requests to check consistency"""
    print("\n" + "=" * 80)
    print("🔄 TESTING MULTIPLE REQUESTS")
    print("=" * 80)
    
    generator = get_gemini_generator()
    
    if not generator.enabled:
        print("\n⚠️  Gemini not enabled, skipping multiple request test")
        return
    
    test_cases = [
        {
            "user_input": "I'm feeling sad",
            "emotion": "sadness",
            "response_plan": {
                "validation": "I hear that you're feeling down.",
                "question": "What's been weighing on your mind?"
            }
        },
        {
            "user_input": "I'm so angry",
            "emotion": "anger",
            "response_plan": {
                "validation": "That sounds really frustrating.",
                "question": "What happened that made you feel this way?"
            }
        },
        {
            "user_input": "I feel great today",
            "emotion": "joy",
            "response_plan": {
                "validation": "That's wonderful to hear!",
                "question": "What's contributing to these positive feelings?"
            }
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} different scenarios...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. Testing: {test_case['user_input']}")
        
        payload = {
            "user_input": test_case['user_input'],
            "emotion": test_case['emotion'],
            "response_plan": test_case['response_plan'],
            "constraints": {"max_sentences": 3, "no_diagnosis": True}
        }
        
        response = await generator.generate_response(payload)
        
        if response:
            print(f"   ✅ {response[:80]}...")
        else:
            print(f"   ⚠️  Fallback used")
        
        # Small delay between requests
        await asyncio.sleep(0.5)
    
    # Final stats
    stats = generator.get_stats()
    print(f"\n📊 Final Statistics:")
    print(f"   Success rate: {stats['success_rate']}")
    print(f"   Avg latency: {stats['avg_latency_ms']}ms")


if __name__ == "__main__":
    asyncio.run(test_gemini())
    asyncio.run(test_multiple_requests())
