"""
Response Builder - Assembles intelligent, context-aware responses
Operates within strict safety constraints - no generative AI
"""

import re
import random
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ResponseComponents:
    """Structured response components"""
    validation: str
    reflection: Optional[str]
    body: str
    question: Optional[str]


class ReflectionExtractor:
    """Lightweight rule-based reflection extraction (<5ms)"""
    
    # Patterns to extract key phrases for reflection
    FEELING_PATTERNS = [
        r"(?:i feel|i'm feeling|feeling)\s+(?:like\s+)?(.{5,50}?)(?:\.|,|$)",
        r"(?:i am|i'm)\s+(?:so\s+)?(.{5,40}?)(?:\.|,|and|$)",
        r"(?:i can't|i cannot)\s+(.{5,40}?)(?:\.|,|$)",
        r"(?:i want to|i wanna)\s+(.{5,40}?)(?:\.|,|$)",
        r"(?:everything|nothing)\s+(?:is|feels?)\s+(.{5,40}?)(?:\.|,|$)",
    ]
    
    def extract(self, text: str) -> Optional[str]:
        """Extract key phrase for reflection"""
        text_lower = text.lower().strip()
        
        # Try each pattern
        for pattern in self.FEELING_PATTERNS:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                phrase = match.group(1).strip()
                # Clean up the phrase
                phrase = self._clean_phrase(phrase)
                if phrase and len(phrase) > 3:
                    return phrase
        
        # Fallback: extract first meaningful clause
        if len(text_lower) > 10:
            # Take first sentence or clause
            first_part = re.split(r'[.!?]', text_lower)[0]
            if 10 < len(first_part) < 60:
                return self._clean_phrase(first_part)
        
        return None
    
    def _clean_phrase(self, phrase: str) -> str:
        """Clean extracted phrase"""
        # Remove trailing conjunctions
        phrase = re.sub(r'\s+(and|but|or|so|because)$', '', phrase)
        # Remove extra whitespace
        phrase = ' '.join(phrase.split())
        return phrase.strip()


class VariationEngine:
    """Controlled variation system for natural language"""
    
    VALIDATION_STARTERS = [
        "I can hear that",
        "I sense that",
        "It sounds like",
        "It seems like",
        "I understand that",
    ]
    
    REFLECTION_FRAMES = [
        "It sounds like you're feeling {phrase}.",
        "I hear that you're feeling {phrase}.",
        "It seems like you're experiencing {phrase}.",
        "I get the sense that you're feeling {phrase}.",
    ]
    
    EMPATHY_PHRASES = [
        "That sounds really hard.",
        "That must be difficult.",
        "I can imagine how challenging that is.",
        "That sounds incredibly tough.",
    ]
    
    QUESTION_STARTERS = [
        "Can you tell me more about",
        "What's been happening with",
        "How long have you been feeling",
        "What do you think is contributing to",
    ]
    
    def __init__(self):
        self.used_variations = {}  # Track usage per session
    
    def get_validation_starter(self, session_id: str) -> str:
        """Get varied validation starter"""
        return self._get_varied(session_id, "validation", self.VALIDATION_STARTERS)
    
    def get_reflection_frame(self, session_id: str) -> str:
        """Get varied reflection frame"""
        return self._get_varied(session_id, "reflection", self.REFLECTION_FRAMES)
    
    def get_empathy_phrase(self, session_id: str) -> str:
        """Get varied empathy phrase"""
        return self._get_varied(session_id, "empathy", self.EMPATHY_PHRASES)
    
    def _get_varied(self, session_id: str, category: str, options: List[str]) -> str:
        """Get variation avoiding recent usage"""
        key = f"{session_id}_{category}"
        
        # Get usage history
        used = self.used_variations.get(key, [])
        
        # Filter out recently used (last 3)
        available = [opt for opt in options if opt not in used[-3:]]
        
        if not available:
            available = options
        
        # Select one
        selected = random.choice(available)
        
        # Update history
        used.append(selected)
        self.used_variations[key] = used[-5:]  # Keep last 5
        
        return selected


class SessionMemory:
    """Lightweight session-level memory for micro-personalization"""
    
    def __init__(self):
        self.themes = {}  # session_id -> set of themes
    
    def extract_themes(self, session_id: str, text: str):
        """Extract and store themes from user text"""
        if session_id not in self.themes:
            self.themes[session_id] = set()
        
        text_lower = text.lower()
        
        # Common themes to track
        theme_keywords = {
            "work": ["work", "job", "boss", "colleague", "office"],
            "school": ["school", "exam", "test", "study", "class", "teacher"],
            "family": ["family", "parent", "mother", "father", "sibling"],
            "relationship": ["relationship", "partner", "boyfriend", "girlfriend", "spouse"],
            "health": ["health", "sick", "pain", "doctor", "hospital"],
            "money": ["money", "financial", "debt", "bills", "afford"],
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                self.themes[session_id].add(theme)
    
    def get_themes(self, session_id: str) -> set:
        """Get stored themes for session"""
        return self.themes.get(session_id, set())
    
    def clear_session(self, session_id: str):
        """Clear session memory"""
        if session_id in self.themes:
            del self.themes[session_id]


class ResponseBuilder:
    """Main response builder - assembles intelligent responses"""
    
    def __init__(self):
        self.reflection_extractor = ReflectionExtractor()
        self.variation_engine = VariationEngine()
        self.session_memory = SessionMemory()
    
    def build_response(
        self,
        base_template: str,
        user_text: str,
        emotion: str,
        intent: str,
        turn_number: int,
        session_id: str,
        context_emotions: List[str] = None
    ) -> str:
        """
        Build enhanced response from base template
        
        Args:
            base_template: Selected template from templates.py
            user_text: Original user input
            emotion: Detected emotion
            intent: Detected intent
            turn_number: Current turn number
            session_id: Session identifier
            context_emotions: List of recent emotions
        
        Returns:
            Enhanced response string
        """
        # Extract themes for future use
        self.session_memory.extract_themes(session_id, user_text)
        
        # Extract reflection phrase
        reflection_phrase = self.reflection_extractor.extract(user_text)
        
        # Build response components
        components = self._build_components(
            base_template,
            reflection_phrase,
            emotion,
            intent,
            turn_number,
            session_id,
            context_emotions
        )
        
        # Assemble final response
        response = self._assemble_response(components, session_id)
        
        # Add micro-personalization if applicable
        response = self._add_personalization(response, session_id, turn_number)
        
        return response
    
    def _build_components(
        self,
        base_template: str,
        reflection_phrase: Optional[str],
        emotion: str,
        intent: str,
        turn_number: int,
        session_id: str,
        context_emotions: List[str]
    ) -> ResponseComponents:
        """Build structured response components"""
        
        # Validation component (emotion acknowledgment)
        validation = self._build_validation(emotion, session_id)
        
        # Reflection component (mirror user's words)
        reflection = None
        if reflection_phrase and turn_number <= 3:
            # Add reflection in early turns
            frame = self.variation_engine.get_reflection_frame(session_id)
            reflection = frame.format(phrase=reflection_phrase)
        
        # Body (main template content)
        body = base_template
        
        # Question component (extracted if present in template)
        question = self._extract_question(base_template)
        if question:
            # Remove question from body to avoid duplication
            body = base_template.replace(question, "").strip()
        
        return ResponseComponents(
            validation=validation,
            reflection=reflection,
            body=body,
            question=question
        )
    
    def _build_validation(self, emotion: str, session_id: str) -> str:
        """Build validation component with variation"""
        starter = self.variation_engine.get_validation_starter(session_id)
        
        emotion_phrases = {
            "sadness": "you're going through something really painful",
            "fear": "you're feeling scared or anxious right now",
            "anger": "you're feeling frustrated or angry",
            "joy": "you're experiencing something positive",
            "neutral": "you're sharing something important",
            "surprise": "something unexpected happened",
            "disgust": "something is really bothering you",
        }
        
        phrase = emotion_phrases.get(emotion, "you're going through something difficult")
        return f"{starter} {phrase}."
    
    def _extract_question(self, template: str) -> Optional[str]:
        """Extract question from template if present"""
        # Find sentences ending with ?
        sentences = re.split(r'(?<=[.!?])\s+', template)
        for sentence in sentences:
            if sentence.strip().endswith('?'):
                return sentence.strip()
        return None
    
    def _assemble_response(self, components: ResponseComponents, session_id: str) -> str:
        """Assemble components into final response"""
        parts = []
        
        # Add validation
        parts.append(components.validation)
        
        # Add reflection if present
        if components.reflection:
            parts.append(components.reflection)
        
        # Add body
        parts.append(components.body)
        
        # Add question if present
        if components.question:
            parts.append(components.question)
        
        return " ".join(parts)
    
    def _add_personalization(self, response: str, session_id: str, turn_number: int) -> str:
        """Add micro-personalization based on session themes"""
        # Only add personalization after turn 2
        if turn_number <= 2:
            return response
        
        themes = self.session_memory.get_themes(session_id)
        
        if not themes:
            return response
        
        # Add contextual phrase based on themes
        theme_phrases = {
            "work": "especially with everything going on at work",
            "school": "especially with your studies and exams",
            "family": "especially with family matters on your mind",
            "relationship": "especially in your relationship",
            "health": "especially while dealing with health concerns",
            "money": "especially with financial pressures",
        }
        
        # Pick one theme to reference
        theme = random.choice(list(themes))
        phrase = theme_phrases.get(theme)
        
        if phrase:
            # Insert before last sentence
            sentences = response.split('. ')
            if len(sentences) > 1:
                sentences[-2] = f"{sentences[-2]}, {phrase}"
                response = '. '.join(sentences)
        
        return response
    
    def clear_session(self, session_id: str):
        """Clear session-specific data"""
        self.session_memory.clear_session(session_id)


# Singleton instance
_response_builder: Optional[ResponseBuilder] = None


def get_response_builder() -> ResponseBuilder:
    """Get singleton response builder instance"""
    global _response_builder
    if _response_builder is None:
        _response_builder = ResponseBuilder()
    return _response_builder
