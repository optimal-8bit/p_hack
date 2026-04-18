#!/usr/bin/env python3
"""
Simple LLM test to debug generation issue
"""

import sys
import os
import asyncio
import logging

# Setup logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from response_engine.llm_generator import get_llm_generator


async def main():
    print("🔍 Simple LLM Generation Test")
    print("=" * 60)
    
    generator = get_llm_generator()
    
    # Check if enabled
    print(f"LLM Enabled: {generator.enabled}")
    print(f"Timeout: {generator.timeout_seconds}s")
    
    # Note: First run takes ~12s (GPU warmup), subsequent runs ~2-3s
    print(f"Note: First generation may take 10-15s for GPU warmup")
    print(f"      Subsequent generations will be 2-3s")
    
    # Simple test payload
    payload = {
        "user_input": "I feel anxious",
        "response_plan": {
            "validation": "That sounds challenging.",
            "question": "Can you tell me more?"
        },
        "constraints": {
            "max_sentences": 3,
            "no_diagnosis": True
        }
    }
    
    print("\nAttempting generation...")
    print(f"Payload: {payload}")
    
    try:
        response = await generator.generate_response(payload)
        
        if response:
            print(f"\n✅ Success!")
            print(f"Response: {response}")
        else:
            print(f"\n❌ Returned None")
            print(f"Stats: {generator.get_stats()}")
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())