#!/usr/bin/env python3
"""
Quick test script for facial emotion detection backend integration
Tests the emotion fusion API without needing the full frontend
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
SESSION_ID = f"test-session-{int(time.time())}"

def log(message, level="INFO"):
    """Log with timestamp and emoji"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "ℹ️")
    print(f"[{timestamp}] {emoji} {message}")

def test_health():
    """Test backend health"""
    try:
        log("Testing backend health...")
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            log(f"Backend is healthy: {data['status']}", "SUCCESS")
            log(f"Models loaded: {data['models_loaded']}")
            return True
        else:
            log(f"Health check failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Health check failed: {e}", "ERROR")
        return False

def test_text_only_chat():
    """Test text-only chat (baseline)"""
    try:
        log("Testing text-only chat...")
        
        payload = {
            "session_id": SESSION_ID,
            "message": "I'm feeling really happy today!"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            log(f"Text-only chat successful", "SUCCESS")
            log(f"Detected emotion: {data['emotion']['emotion']} ({data['emotion']['confidence']:.3f})")
            log(f"Response: {data['response_text'][:100]}...")
            return True
        else:
            log(f"Text-only chat failed: {response.status_code}", "ERROR")
            log(f"Response: {response.text}")
            return False
    except Exception as e:
        log(f"Text-only chat failed: {e}", "ERROR")
        return False

def test_multimodal_congruent():
    """Test multimodal chat with congruent emotions"""
    try:
        log("Testing multimodal chat (congruent emotions)...")
        
        payload = {
            "session_id": SESSION_ID,
            "message": "I'm feeling really happy today!",
            "facial_emotion": {
                "dominant_emotion": "happy",
                "confidence": 0.95,
                "all_emotions": {
                    "happy": 0.95,
                    "neutral": 0.03,
                    "sad": 0.01,
                    "angry": 0.005,
                    "fearful": 0.003,
                    "surprised": 0.001,
                    "disgusted": 0.001
                },
                "age": 27,
                "gender": "female",
                "timestamp": time.time() * 1000
            }
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            log(f"Multimodal congruent test successful", "SUCCESS")
            log(f"Text emotion: {data['emotion']['emotion']} ({data['emotion']['confidence']:.3f})")
            log(f"Facial emotion: {data['emotion'].get('facial_emotion', 'N/A')}")
            log(f"Is multimodal: {data['emotion'].get('is_multimodal', False)}")
            log(f"Congruence: {data['emotion'].get('emotion_congruence', 'N/A')}")
            log(f"Response: {data['response_text'][:100]}...")
            
            if data['emotion'].get('emotion_congruence') == 'congruent':
                log("✓ Congruence correctly detected", "SUCCESS")
            else:
                log("✗ Expected congruent emotions", "WARNING")
            
            return True
        else:
            log(f"Multimodal congruent test failed: {response.status_code}", "ERROR")
            log(f"Response: {response.text}")
            return False
    except Exception as e:
        log(f"Multimodal congruent test failed: {e}", "ERROR")
        return False

def test_multimodal_incongruent():
    """Test multimodal chat with incongruent emotions"""
    try:
        log("Testing multimodal chat (incongruent emotions)...")
        
        payload = {
            "session_id": SESSION_ID,
            "message": "I'm fine, everything is okay.",
            "facial_emotion": {
                "dominant_emotion": "sad",
                "confidence": 0.87,
                "all_emotions": {
                    "sad": 0.87,
                    "neutral": 0.08,
                    "happy": 0.03,
                    "angry": 0.01,
                    "fearful": 0.005,
                    "surprised": 0.003,
                    "disgusted": 0.002
                },
                "age": 27,
                "gender": "female",
                "timestamp": time.time() * 1000
            }
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            log(f"Multimodal incongruent test successful", "SUCCESS")
            log(f"Text emotion: {data['emotion']['emotion']} ({data['emotion']['confidence']:.3f})")
            log(f"Facial emotion: {data['emotion'].get('facial_emotion', 'N/A')}")
            log(f"Is multimodal: {data['emotion'].get('is_multimodal', False)}")
            log(f"Congruence: {data['emotion'].get('emotion_congruence', 'N/A')}")
            log(f"Response: {data['response_text'][:100]}...")
            
            if data['emotion'].get('emotion_congruence') == 'incongruent':
                log("✓ Incongruence correctly detected", "SUCCESS")
            else:
                log("✗ Expected incongruent emotions", "WARNING")
            
            return True
        else:
            log(f"Multimodal incongruent test failed: {response.status_code}", "ERROR")
            log(f"Response: {response.text}")
            return False
    except Exception as e:
        log(f"Multimodal incongruent test failed: {e}", "ERROR")
        return False

def test_edge_cases():
    """Test edge cases"""
    try:
        log("Testing edge cases...")
        
        # Test with very low confidence facial emotion
        payload = {
            "session_id": SESSION_ID,
            "message": "I'm not sure how I feel.",
            "facial_emotion": {
                "dominant_emotion": "neutral",
                "confidence": 0.35,  # Low confidence
                "all_emotions": {
                    "neutral": 0.35,
                    "happy": 0.20,
                    "sad": 0.18,
                    "angry": 0.12,
                    "fearful": 0.08,
                    "surprised": 0.04,
                    "disgusted": 0.03
                },
                "age": 27,
                "gender": "female",
                "timestamp": time.time() * 1000
            }
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            log(f"Edge case test successful", "SUCCESS")
            log(f"Congruence with low confidence: {data['emotion'].get('emotion_congruence', 'N/A')}")
            return True
        else:
            log(f"Edge case test failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Edge case test failed: {e}", "ERROR")
        return False

def main():
    """Run all tests"""
    log("🚀 Starting facial emotion detection backend tests...")
    log(f"Backend URL: {BACKEND_URL}")
    log(f"Session ID: {SESSION_ID}")
    print()
    
    tests = [
        ("Backend Health", test_health),
        ("Text-Only Chat", test_text_only_chat),
        ("Multimodal Congruent", test_multimodal_congruent),
        ("Multimodal Incongruent", test_multimodal_incongruent),
        ("Edge Cases", test_edge_cases)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        log(f"Running test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                log(f"✅ {test_name} PASSED", "SUCCESS")
            else:
                log(f"❌ {test_name} FAILED", "ERROR")
        except Exception as e:
            log(f"❌ {test_name} CRASHED: {e}", "ERROR")
            results.append((test_name, False))
        
        print("-" * 60)
    
    # Summary
    print()
    log("📊 TEST SUMMARY:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        log(f"  {test_name}: {status}")
    
    print()
    if passed == total:
        log(f"🎉 ALL TESTS PASSED ({passed}/{total})", "SUCCESS")
        log("Facial emotion detection is working correctly!")
    else:
        log(f"⚠️ SOME TESTS FAILED ({passed}/{total})", "WARNING")
        log("Check the backend logs and ensure all models are loaded.")
    
    print()
    log("💡 Next steps:")
    log("1. If tests passed, try the HTML test page: test_facial_emotion.html")
    log("2. Start the React frontend and test the full integration")
    log("3. Check browser console for detailed facial emotion logs")

if __name__ == "__main__":
    main()