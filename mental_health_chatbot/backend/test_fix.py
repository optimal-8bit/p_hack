#!/usr/bin/env python3
"""Quick test to verify the therapeutic response fix"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from response_engine.payload_builder import get_payload_builder
from response_engine.gemini_generator import get_gemini_generator

async def test_fix():
    print("🧪 Testing Therapeutic Response Fix")
    print("=" * 60)
    
    # Build payload
    payload_builder = get_payload_builder()
    generator = get_gemini_generator()
    
    # Test case: "I am little sad today"
    print("\n📝 Test Input: 'I am little sad today'")
    print("-" * 40)
    
    llm_payload = payload_builder.build_llm_payload(
        user_input="I am little sad today",
        processed_text="I am little sad today",
        message_type={"type": "emotional", "confidence": 0.8},
        emotion="sadness",
        emotion_confidence=0.85,
        intent="depression and sadness",
        intent_confidence=0.75,
        turn_number=1,
        context=[],
        response_components={},
        allow_therapist=True
    )
    
    # Check payload structure
    print("\n✅ Payload Structure:")
    print(f"  - Has intervention_plan: {'intervention_plan' in llm_payload}")
    print(f"  - Has therapeutic_strategy: {'therapeutic_strategy' in llm_payload}")
    print(f"  - Has session_info: {'session_info' in llm_payload}")
    
    if 'intervention_plan' in llm_payload:
        plan = llm_payload['intervention_plan']
        print(f"\n📋 Intervention Plan:")
        for key in plan.keys():
            print(f"  - {key}: {plan[key][:50]}..." if len(str(plan[key])) > 50 else f"  - {key}: {plan[key]}")
    
    if 'therapeutic_strategy' in llm_payload:
        strategy = llm_payload['therapeutic_strategy']
        print(f"\n🎯 Therapeutic Strategy:")
        print(f"  - Modality: {strategy.get('primary_modality')}")
        print(f"  - Techniques: {strategy.get('techniques')}")
        print(f"  - Focus: {strategy.get('therapeutic_focus')}")
    
    # Try to generate response
    print("\n🤖 Attempting Gemini Generation...")
    response = await generator.generate_response(llm_payload)
    
    if response:
        print(f"\n✅ SUCCESS! Generated Therapeutic Response:")
        print(f"   {response}")
        print(f"\n📊 Response Stats:")
        print(f"   - Words: {len(response.split())}")
        print(f"   - Sentences: {len([s for s in response.split('.') if s.strip()])}")
    else:
        print("\n❌ FAILED: Using fallback (check API key and logs)")
    
    # Show stats
    stats = generator.get_stats()
    print(f"\n📈 Generator Stats:")
    for key, value in stats.items():
        print(f"   - {key}: {value}")

if __name__ == "__main__":
    asyncio.run(test_fix())
