import pytest
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint_returns_200():
    """Test health endpoint is accessible"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "models_loaded" in data
    assert "version" in data


def test_chat_endpoint_normal_message():
    """Test chat endpoint with normal message"""
    response = client.post(
        "/api/chat",
        json={
            "session_id": "test_session_1",
            "message": "I'm feeling a bit sad today"
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "response_text" in data
    assert "emotion" in data
    assert "intent" in data
    assert "is_crisis" in data
    assert data["is_crisis"] == False
    assert len(data["response_text"]) > 0


def test_chat_endpoint_crisis_message():
    """Test chat endpoint detects crisis"""
    response = client.post(
        "/api/chat",
        json={
            "session_id": "test_session_crisis",
            "message": "I want to kill myself"
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_crisis"] == True
    assert "9152987821" in data["response_text"]  # Helpline number
    assert "112" in data["response_text"]  # Emergency number


def test_chat_endpoint_empty_message_rejected():
    """Test chat endpoint rejects empty messages"""
    response = client.post(
        "/api/chat",
        json={
            "session_id": "test_session_2",
            "message": ""
        }
    )
    
    # Should return 422 validation error
    assert response.status_code == 422


def test_chat_endpoint_missing_session_id():
    """Test chat endpoint requires session_id"""
    response = client.post(
        "/api/chat",
        json={
            "message": "Hello"
        }
    )
    
    assert response.status_code == 422


def test_session_history_endpoint():
    """Test session history endpoint"""
    session_id = "test_history_session"
    
    # Send a message first
    client.post(
        "/api/chat",
        json={
            "session_id": session_id,
            "message": "Test message"
        }
    )
    
    # Get history
    response = client.get(f"/api/session/{session_id}/history")
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert "turns" in data
    assert "total_turns" in data


def test_clear_session_endpoint():
    """Test clear session endpoint"""
    session_id = "test_clear_session"
    
    # Send a message first
    client.post(
        "/api/chat",
        json={
            "session_id": session_id,
            "message": "Test message"
        }
    )
    
    # Clear session
    response = client.delete(f"/api/session/{session_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "cleared"
    assert data["session_id"] == session_id


def test_supported_languages_endpoint():
    """Test supported languages endpoint"""
    response = client.get("/api/supported-languages")
    assert response.status_code == 200
    
    data = response.json()
    assert "languages" in data
    assert len(data["languages"]) > 0
    
    # Check structure
    for lang in data["languages"]:
        assert "code" in lang
        assert "name" in lang


def test_root_endpoint():
    """Test root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_chat_endpoint_multiple_turns():
    """Test multiple turns in same session"""
    session_id = "test_multi_turn"
    
    messages = [
        "I'm feeling sad",
        "I can't stop crying",
        "Nothing makes me happy anymore"
    ]
    
    for i, message in enumerate(messages, 1):
        response = client.post(
            "/api/chat",
            json={
                "session_id": session_id,
                "message": message
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["turn_number"] == i


def test_chat_endpoint_processing_time():
    """Test that processing time is reported"""
    response = client.post(
        "/api/chat",
        json={
            "session_id": "test_timing",
            "message": "Hello"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "processing_time_ms" in data
    assert data["processing_time_ms"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
