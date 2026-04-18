import logging
import time
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)

SESSION_TIMEOUT = 1800  # 30 minutes in seconds


@dataclass
class TurnRecord:
    user_text: str
    emotion: str
    intent: str
    response_template_key: str
    turn_number: int
    timestamp: float
    language: str = "en"  # Track language per turn


class ContextTracker:
    def __init__(self):
        self.sessions: Dict[str, deque] = {}
        self.turn_counts: Dict[str, int] = defaultdict(int)
        self.last_access: Dict[str, float] = {}
    
    def add_turn(self, session_id: str, turn_record: TurnRecord):
        """Add a turn to session history"""
        # Initialize session if needed
        if session_id not in self.sessions:
            self.sessions[session_id] = deque(maxlen=config.CONTEXT_WINDOW_SIZE)
        
        # Add turn
        self.sessions[session_id].append(turn_record)
        self.turn_counts[session_id] = turn_record.turn_number
        self.last_access[session_id] = time.time()
        
        logger.debug(f"Added turn {turn_record.turn_number} to session {session_id}")
    
    def get_context(self, session_id: str) -> List[TurnRecord]:
        """Get conversation history for session"""
        self._check_expiry(session_id)
        
        if session_id not in self.sessions:
            return []
        
        self.last_access[session_id] = time.time()
        return list(self.sessions[session_id])
    
    def get_turn_number(self, session_id: str) -> int:
        """Get current turn count for session (1-indexed)"""
        self._check_expiry(session_id)
        
        self.last_access[session_id] = time.time()
        return self.turn_counts[session_id] + 1
    
    def get_last_language(self, session_id: str) -> str:
        """Get language from last turn"""
        context = self.get_context(session_id)
        if context:
            return context[-1].language
        return "en"  # Default to English
    
    def get_dominant_emotion(self, session_id: str) -> Optional[str]:
        """Get most frequent emotion across last N turns"""
        context = self.get_context(session_id)
        
        if not context:
            return None
        
        # Count emotions
        emotion_counts = defaultdict(int)
        for turn in context:
            emotion_counts[turn.emotion] += 1
        
        # Return most common
        return max(emotion_counts, key=emotion_counts.get)
    
    def get_last_intent(self, session_id: str) -> Optional[str]:
        """Get intent from last turn"""
        context = self.get_context(session_id)
        if context:
            return context[-1].intent
        return None
    
    def clear_session(self, session_id: str):
        """Clear session memory"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.turn_counts:
            del self.turn_counts[session_id]
        if session_id in self.last_access:
            del self.last_access[session_id]
        
        # Also clear advanced response builder session data
        from response_engine.advanced_response_builder import get_advanced_response_builder
        advanced_builder = get_advanced_response_builder()
        advanced_builder.clear_session(session_id)
        
        logger.info(f"Cleared session: {session_id}")
    
    def _check_expiry(self, session_id: str):
        """Check if session has expired and clear if needed"""
        if session_id in self.last_access:
            elapsed = time.time() - self.last_access[session_id]
            if elapsed > SESSION_TIMEOUT:
                logger.info(f"Session {session_id} expired after {elapsed:.0f}s")
                self.clear_session(session_id)


# Singleton instance
_context_tracker: Optional[ContextTracker] = None


def get_context_tracker() -> ContextTracker:
    """Get singleton context tracker instance"""
    global _context_tracker
    if _context_tracker is None:
        _context_tracker = ContextTracker()
    return _context_tracker
