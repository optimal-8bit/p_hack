"""
Simple test script for prescription API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"
SESSION_ID = "test-session-456"

print("=" * 60)
print("PRESCRIPTION API SIMPLE TEST")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"✓ Status: {response.status_code}")
    print(f"  Response: {response.json()}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 2: Get reminders (should be empty initially)
print(f"\n2. Getting reminders for session: {SESSION_ID}")
try:
    response = requests.get(f"{BASE_URL}/api/prescription/reminders/{SESSION_ID}")
    print(f"✓ Status: {response.status_code}")
    reminders = response.json()
    print(f"  Found {len(reminders)} reminders")
    if reminders:
        for r in reminders:
            print(f"    - {r['medicine_name']} at {r['time']}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Manually create a reminder using database function
print("\n3. Testing direct reminder creation...")
print("  (This would normally be done through prescription upload)")
print("  For now, upload a prescription through the frontend to test the full flow")

print("\n" + "=" * 60)
print("INSTRUCTIONS:")
print("=" * 60)
print(f"1. Open the frontend: http://localhost:5173")
print(f"2. Click the pill icon (💊) in chat")
print(f"3. Upload any image file")
print(f"4. Review the extracted medicines (mock data)")
print(f"5. Click 'Create Reminder Schedule'")
print(f"6. Go to Medicine Reminder page")
print(f"7. Check browser console for logs")
print(f"\nYour session ID: {SESSION_ID}")
print("(Or it will use the one from localStorage)")
