#!/usr/bin/env python3
"""
Test script for the new therapeutic response system
"""

import asyncio
import os
import sys
import logging

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from response_engine.gemini_generator import get_gemini_generator
from response_engine.payload_builder import get_payload_builder

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_therapeutic_responses():
    """Test the new therapeutic response system"""
    
    print("🧠 Testing Expert Therapist Response System")
    print("=" * 60)
    
    # Initialize components
    generator = get_gemini_generator()
    payload_builder = get_payload_builder()
    
    # Test cases representing different therapeutic scenarios
    test_cases = [
        {
            "user_input": "I've been feeling really anxious lately and can't sleep",
            "emotion": "anxiety",
            "intent": "anxiety and panic",
            "description": "Anxiety Management"
        },
        {
            "user_input": "I feel like nothing I do matters anymore",
            "emotion": "sadness", 
            "intent": "depression and sadness",
            "description": "Depression Support"
        },
        {
            "user_input": "My partner and I keep fighting about everything",
            "emotion": "anger",
            "intent": "relationship issues", 
            "description": "Relationship Therapy"
        },
        {
            "user_input": "I'm overwhelmed with work and feel like I'm failing",
            "emotion": "fear",
            "intent": "work stress",
            "description": "Stress Management"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {case['description']}")
        print(f"User Input: \"{case['user_input']}\"")
        print(f"Detected: {case['emotion']} / {case['intent']}")
        print("-" * 40)
        
        try:
            # Build therapeutic payload
            llm_payload = payload_builder.build_llm_payload(
                user_input=case['user_input'],
                processed_text=case['user_input'],
                message_type={"type": "emotional", "confidence": 0.8},
                emotion=case['emotion'],
                emotion_confidence=0.85,
                intent=case['intent'],
                intent_confidence=0.80,
                turn_number=2,
                context=[],  # Empty context for simplicity
                response_components={},  # Will be built by payload builder
                allow_therapist=True
            )
            
            # Generate therapeutic response
            response = await generator.generate_response(llm_payload)
            
            if response:
                print(f"✅ Therapeutic Response:")
                print(f"   {response}")
                print(f"   Length: {len(response.split())} words")
            else:
                print("❌ No response generated (using fallback)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    # Print generator statistics
    stats = generator.get_stats()
    print("📊 Generator Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

async def test_multimodal_input():
    """Test with multimodal input (text + emotion from audio/video)"""
    
    print("\n🎥 Testing Multimodal Therapeutic Response")
    print("=" * 60)
    
    generator = get_gemini_generator()
    payload_builder = get_payload_builder()
    
    # Simulate multimodal input where text and detected emotion might differ
    case = {
        "user_input": "I'm fine, everything is okay",  # Text says fine
        "detected_emotion": "sadness",  # But voice/face shows sadness
        "intent": "emotional suppression"
    }
    
    print(f"Text Input: \"{case['user_input']}\"")
    print(f"Detected Emotion (Audio/Video): {case['detected_emotion']}")
    print("-" * 40)
    
    try:
        llm_payload = payload_builder.build_llm_payload(
            user_input=case['user_input'],
            processed_text=case['user_input'],
            message_type={"type": "emotional", "confidence": 0.9},
            emotion=case['detected_emotion'],  # Use multimodal emotion
            emotion_confidence=0.90,
            intent=case['intent'],
            intent_confidence=0.75,
            turn_number=3,
            context=[],
            response_components={},
            allow_therapist=True
        )
        
        response = await generator.generate_response(llm_payload)
        
        if response:
            print(f"✅ Therapeutic Response (addressing incongruence):")
            print(f"   {response}")
        else:
            print("❌ No response generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    
    # Check if Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not set - responses will use template fallback")
        print("   Set your API key to test the full therapeutic system")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print()
    
    # Run tests
    asyncio.run(test_therapeutic_responses())
    asyncio.run(test_multimodal_input())
    
    print("\n✅ Therapeutic response testing complete!")
    print("\n💡 Next steps:")
    print("   1. Start your backend: python main.py")
    print("   2. Test in the web interface with real conversations")
    print("   3. Monitor the logs for therapeutic response quality")

if __name__ == "__main__":
    main()