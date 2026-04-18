#!/usr/bin/env python3
"""
Quick verification script for doctor recommendation setup
Run this to check if everything is configured correctly
"""

import os
import sys

def check_file(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"  ✅ {description}")
        return True
    else:
        print(f"  ❌ {description} - NOT FOUND: {path}")
        return False

def main():
    print("=" * 60)
    print("Doctor Recommendation Setup Verification")
    print("=" * 60)
    
    all_good = True
    
    # Backend files
    print("\n📦 Backend Files:")
    all_good &= check_file("mental_health_chatbot/backend/database/doctor_models.py", "Doctor models")
    all_good &= check_file("mental_health_chatbot/backend/api/doctor_routes.py", "Doctor API routes")
    all_good &= check_file("mental_health_chatbot/backend/services/doctor_recommendation_service.py", "Recommendation service")
    all_good &= check_file("mental_health_chatbot/backend/seed_doctors.py", "Seed script")
    
    # Frontend files
    print("\n🎨 Frontend Files:")
    all_good &= check_file("react_web/src/services/api.service.js", "API client")
    all_good &= check_file("react_web/src/services/doctor.service.js", "Doctor service")
    all_good &= check_file("react_web/src/components/chat/DoctorRecommendation.jsx", "Recommendation component")
    
    # Documentation
    print("\n📚 Documentation:")
    all_good &= check_file("QUICK_START.md", "Quick start guide")
    all_good &= check_file("TEST_DOCTOR_RECOMMENDATIONS.md", "Testing guide")
    all_good &= check_file("SETUP_CHECKLIST.md", "Setup checklist")
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("✅ All files present!")
        print("\n🚀 Next Steps:")
        print("1. cd mental_health_chatbot/backend")
        print("2. python seed_doctors.py")
        print("3. python main.py")
        print("4. Open new terminal: cd react_web && npm run dev")
        print("5. Test: http://localhost:8000/api/test-recommendation")
        print("6. Chat: http://localhost:5173/mental-health-chat")
        print("\n💡 Type messages with 'anxious', 'depressed', 'can't sleep'")
        print("   After 2-3 messages, recommendation should appear!")
        print("\n📖 Read TEST_DOCTOR_RECOMMENDATIONS.md for detailed testing")
        return 0
    else:
        print("❌ Some files are missing!")
        print("\n⚠️  Please check the file paths above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
