#!/usr/bin/env python3
"""
Quick test to see if backend starts without errors
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mental_health_chatbot', 'backend'))

def test_imports():
    """Test if all imports work"""
    try:
        print("Testing imports...")
        
        # Test schemas
        from api.schemas import ChatRequest, ChatResponseSchema, DoctorRecommendationInfo
        print("✅ Schemas imported successfully")
        
        # Test doctor routes
        from api.doctor_routes import router
        print("✅ Doctor routes imported successfully")
        
        # Test main routes
        from api.routes import router as main_router
        print("✅ Main routes imported successfully")
        
        print("\n🎉 All imports successful! Backend should start now.")
        print("\nRun: cd mental_health_chatbot/backend && python main.py")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)