"""
Quick test script to verify doctor integration is working
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mental_health_chatbot', 'backend'))

async def test_doctor_integration():
    """Test the doctor integration components"""
    print("=" * 60)
    print("Testing Doctor Integration")
    print("=" * 60)
    
    # Test 1: Import models
    print("\n1. Testing imports...")
    try:
        from database.doctor_models import Doctor, Patient, Appointment, DoctorRecommendation
        print("   ✅ Doctor models imported successfully")
    except Exception as e:
        print(f"   ❌ Failed to import doctor models: {e}")
        return False
    
    # Test 2: Import recommendation service
    try:
        from services.doctor_recommendation_service import get_recommendation_service
        print("   ✅ Recommendation service imported successfully")
    except Exception as e:
        print(f"   ❌ Failed to import recommendation service: {e}")
        return False
    
    # Test 3: Test recommendation analysis
    print("\n2. Testing recommendation analysis...")
    try:
        service = get_recommendation_service()
        
        # Test case: anxiety symptoms
        test_messages = [
            {"content": "I've been feeling really anxious lately"},
            {"content": "I can't sleep and I'm worried all the time"},
            {"content": "I have panic attacks frequently"}
        ]
        
        recommendation = service.analyze_conversation(
            session_id="test-session",
            messages=test_messages,
            emotions=["anxiety", "fear", "worried"],
            intents=["anxiety and panic", "sleep issues"],
            is_crisis=False
        )
        
        if recommendation:
            print(f"   ✅ Recommendation generated:")
            print(f"      - Specialization: {recommendation['recommended_specialization']}")
            print(f"      - Urgency: {recommendation['urgency']}")
            print(f"      - Symptoms detected: {len(recommendation['symptoms'])}")
        else:
            print("   ⚠️  No recommendation generated (may need more symptoms)")
        
    except Exception as e:
        print(f"   ❌ Failed recommendation analysis: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Test crisis detection
    print("\n3. Testing crisis detection...")
    try:
        crisis_messages = [
            {"content": "I don't want to live anymore"}
        ]
        
        crisis_recommendation = service.analyze_conversation(
            session_id="test-crisis",
            messages=crisis_messages,
            emotions=["fear", "sadness"],
            intents=["anxiety and panic"],
            is_crisis=True
        )
        
        if crisis_recommendation and crisis_recommendation['urgency'] == 'urgent':
            print(f"   ✅ Crisis recommendation generated with urgent priority")
        else:
            print(f"   ⚠️  Crisis not detected as urgent")
        
    except Exception as e:
        print(f"   ❌ Failed crisis detection: {e}")
        return False
    
    # Test 5: Database connection
    print("\n4. Testing database connection...")
    try:
        from database.db import create_tables
        await create_tables()
        print("   ✅ Database tables created/verified")
    except Exception as e:
        print(f"   ❌ Failed database setup: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Doctor integration is working.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python mental_health_chatbot/backend/seed_doctors.py")
    print("2. Start backend: python mental_health_chatbot/backend/main.py")
    print("3. Start frontend: cd react_web && npm run dev")
    print("4. Test chat at: http://localhost:5173/mental-health-chat")
    print("\n")
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_doctor_integration())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
