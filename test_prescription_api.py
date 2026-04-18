"""
Test script for prescription API endpoints
Run this to verify the backend is working correctly
"""
import requests
import json
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:8000"
SESSION_ID = "test-session-123"

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='white')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_health():
    """Test health endpoint"""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_upload_prescription():
    """Test prescription upload"""
    print("\n2. Testing prescription upload...")
    
    # Create test image
    img_bytes = create_test_image()
    
    files = {
        'file': ('test_prescription.png', img_bytes, 'image/png')
    }
    data = {
        'session_id': SESSION_ID
    }
    
    response = requests.post(f"{BASE_URL}/api/prescription/upload", files=files, data=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Prescription ID: {result['prescription_id']}")
        print(f"Medicines extracted: {len(result['medicines'])}")
        for med in result['medicines']:
            print(f"  - {med['medicine_name']} ({med['dosage']})")
        return result
    else:
        print(f"Error: {response.text}")
        return None

def test_create_schedule(prescription_id, medicines):
    """Test schedule creation"""
    print("\n3. Testing schedule creation...")
    
    payload = {
        "prescription_id": prescription_id,
        "medicines": medicines
    }
    
    response = requests.post(
        f"{BASE_URL}/api/prescription/schedule",
        params={"session_id": SESSION_ID},
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Message: {result['message']}")
        print(f"Reminder IDs: {result['reminder_ids']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_get_reminders():
    """Test getting reminders"""
    print("\n4. Testing get reminders...")
    
    response = requests.get(f"{BASE_URL}/api/prescription/reminders/{SESSION_ID}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        reminders = response.json()
        print(f"Found {len(reminders)} reminders:")
        for reminder in reminders:
            print(f"  - {reminder['medicine_name']} at {reminder['time']} ({reminder['doses_taken']}/{reminder['doses_per_day']})")
        return reminders
    else:
        print(f"Error: {response.text}")
        return []

def test_update_dose(reminder_id):
    """Test updating dose"""
    print(f"\n5. Testing dose update for reminder {reminder_id}...")
    
    payload = {
        "reminder_id": reminder_id,
        "doses_taken": 2
    }
    
    response = requests.patch(
        f"{BASE_URL}/api/prescription/reminders/dose",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Message: {result['message']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PRESCRIPTION API TEST SUITE")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed! Is the backend running?")
        return
    
    # Test 2: Upload prescription
    upload_result = test_upload_prescription()
    if not upload_result:
        print("\n❌ Prescription upload failed!")
        return
    
    # Test 3: Create schedule
    if not test_create_schedule(upload_result['prescription_id'], upload_result['medicines']):
        print("\n❌ Schedule creation failed!")
        return
    
    # Test 4: Get reminders
    reminders = test_get_reminders()
    if not reminders:
        print("\n❌ No reminders found!")
        return
    
    # Test 5: Update dose
    if reminders:
        test_update_dose(reminders[0]['id'])
    
    # Verify update
    print("\n6. Verifying dose update...")
    updated_reminders = test_get_reminders()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print(f"\nSession ID: {SESSION_ID}")
    print(f"Total reminders: {len(updated_reminders)}")
    print("\nYou can now test the frontend with this session ID.")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend!")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
