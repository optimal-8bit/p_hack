import pytest
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from pipeline.safety import get_safety_checker
from pipeline.preprocessor import get_preprocessor
from pipeline.context_tracker import get_context_tracker, TurnRecord
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from response_engine.template_selector import get_template_selector


def test_safety_detects_crisis_keywords():
    """Test that safety checker detects crisis patterns"""
    checker = get_safety_checker()
    
    crisis_messages = [
        "I want to kill myself",
        "I'm going to end my life",
        "I want to die",
        "I'm thinking about suicide",
        "I want to hurt myself"
    ]
    
    for message in crisis_messages:
        result = checker.check(message)
        assert result.is_crisis, f"Failed to detect crisis in: {message}"
        assert result.response is not None
        assert "9152987821" in result.response  # Check for helpline number


def test_safety_passes_normal_message():
    """Test that safety checker passes normal messages"""
    checker = get_safety_checker()
    
    normal_messages = [
        "I'm feeling a bit sad today",
        "I had a rough day at work",
        "I'm worried about my exam",
        "I feel lonely sometimes"
    ]
    
    for message in normal_messages:
        result = checker.check(message)
        assert not result.is_crisis, f"False positive for: {message}"


def test_preprocessor_cleans_text():
    """Test text cleaning and preprocessing"""
    preprocessor = get_preprocessor()
    
    # Test URL removal
    text_with_url = "Check this out http://example.com I'm feeling sad"
    result = preprocessor.preprocess(text_with_url)
    assert "http://" not in result.cleaned
    
    # Test whitespace normalization
    text_with_spaces = "I'm    feeling    really     sad"
    result = preprocessor.preprocess(text_with_spaces)
    assert "    " not in result.cleaned
    
    # Test truncation
    long_text = "a" * 600
    result = preprocessor.preprocess(long_text)
    assert len(result.cleaned) <= 512


def test_preprocessor_detects_english():
    """Test language detection for English"""
    preprocessor = get_preprocessor()
    
    english_text = "I am feeling very sad and hopeless today"
    result = preprocessor.preprocess(english_text)
    
    assert result.language == "en"
    assert not result.was_translated
    assert result.english_text == result.cleaned


def test_emotion_classifier_returns_valid_result():
    """Test emotion classifier returns valid structure"""
    model = get_emotion_model()
    
    test_text = "I feel really sad and hopeless"
    result = model.predict(test_text)
    
    assert "emotion" in result
    assert "confidence" in result
    assert "all_scores" in result
    assert result["emotion"] in ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
    assert 0 <= result["confidence"] <= 1


def test_emotion_classifier_rule_based_fallback():
    """Test rule-based emotion detection"""
    model = get_emotion_model()
    
    # Test sadness keywords
    sad_text = "I feel so sad and depressed and hopeless"
    result = model.predict(sad_text)
    # Should detect sadness (either via ONNX or rule-based)
    assert result["emotion"] in ["sadness", "fear", "neutral"]
    
    # Test joy keywords
    happy_text = "I feel so happy and excited and wonderful"
    result = model.predict(happy_text)
    assert result["emotion"] in ["joy", "neutral"]


def test_intent_classifier_returns_valid_result():
    """Test intent classifier returns valid structure"""
    model = get_intent_model()
    
    test_text = "I feel really anxious and worried all the time"
    result = model.predict(test_text)
    
    assert "intent" in result
    assert "confidence" in result
    assert "all_scores" in result
    assert 0 <= result["confidence"] <= 1


def test_intent_classifier_rule_based_fallback():
    """Test rule-based intent detection"""
    model = get_intent_model()
    
    # Test anxiety keywords
    anxiety_text = "I feel so anxious and panicked and worried"
    result = model.predict(anxiety_text)
    # Should detect anxiety-related intent
    assert "anxiety" in result["intent"].lower() or "support" in result["intent"].lower()


def test_template_selector_returns_string():
    """Test template selector returns valid responses"""
    selector = get_template_selector()
    
    # Test various emotion/intent combinations
    test_cases = [
        ("sadness", "sadness and depression", 1),
        ("fear", "anxiety and panic", 2),
        ("anger", "anger and frustration", 3),
        ("neutral", "general emotional support", 1),
        ("joy", "general emotional support", 1),
    ]
    
    for emotion, intent, turn_number in test_cases:
        response = selector.select(emotion, intent, turn_number, [], "en")
        assert isinstance(response, str)
        assert len(response) > 0


def test_context_tracker_turn_counting():
    """Test context tracker increments turn numbers correctly"""
    tracker = get_context_tracker()
    session_id = "test_session_123"
    
    # Clear any existing session
    tracker.clear_session(session_id)
    
    # First turn should be 1
    assert tracker.get_turn_number(session_id) == 1
    
    # Add a turn
    turn = TurnRecord(
        user_text="test",
        emotion="neutral",
        intent="general emotional support",
        response_template_key="test",
        turn_number=1,
        timestamp=0.0
    )
    tracker.add_turn(session_id, turn)
    
    # Next turn should be 2
    assert tracker.get_turn_number(session_id) == 2


def test_context_tracker_session_expiry():
    """Test session expiry logic"""
    tracker = get_context_tracker()
    session_id = "test_expiry_session"
    
    # Clear session
    tracker.clear_session(session_id)
    
    # Add a turn with old timestamp
    turn = TurnRecord(
        user_text="test",
        emotion="neutral",
        intent="general emotional support",
        response_template_key="test",
        turn_number=1,
        timestamp=0.0  # Very old timestamp
    )
    tracker.add_turn(session_id, turn)
    
    # Access with expiry check should clear the session
    context = tracker.get_context(session_id)
    # After expiry, context should be empty
    assert len(context) == 0


def test_context_tracker_dominant_emotion():
    """Test dominant emotion calculation"""
    tracker = get_context_tracker()
    session_id = "test_dominant_session"
    
    tracker.clear_session(session_id)
    
    # Add multiple turns with same emotion
    for i in range(3):
        turn = TurnRecord(
            user_text="test",
            emotion="sadness",
            intent="general emotional support",
            response_template_key="test",
            turn_number=i+1,
            timestamp=1000000.0  # Recent timestamp
        )
        tracker.add_turn(session_id, turn)
    
    dominant = tracker.get_dominant_emotion(session_id)
    assert dominant == "sadness"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
