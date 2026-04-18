"""
Advanced Response Builder - Highly realistic, emotionally intelligent responses
Implements structured component assembly with variation and context awareness
"""

import random
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from response_engine.reflection import generate_reflection


@dataclass
class ResponseComponents:
    """Structured response components for assembly"""
    validation: str
    reflection: Optional[str]
    normalization: Optional[str]
    coping: Optional[str]
    gentle_guidance: Optional[str]
    question: str


class VariationEngine:
    """Advanced variation system with usage tracking"""
    
    VALIDATION_VARIANTS = [
        "That sounds really hard.",
        "That must be really tough to deal with.",
        "I can imagine how difficult that feels.",
        "That sounds incredibly challenging.",
        "I hear how much you're struggling with this.",
        "That must be so draining.",
        "I can sense how heavy this feels for you.",
    ]
    
    REFLECTION_STARTERS = [
        "It feels like",
        "It seems like", 
        "It sounds like",
        "I get the sense that",
        "From what you're sharing,",
    ]
    
    NORMALIZATION_PHRASES = [
        "What you're feeling makes complete sense.",
        "It's completely understandable to feel this way.",
        "Anyone in your situation would struggle with this.",
        "These feelings are a natural response to what you're going through.",
        "You're not alone in feeling like this.",
    ]
    
    GENTLE_GUIDANCE = [
        "Sometimes when we're in pain, it helps to take things one moment at a time.",
        "Being gentle with yourself right now might be important.",
        "It's okay to not have all the answers right now.",
        "Taking care of yourself in small ways can make a difference.",
        "Remember that feelings, even painful ones, do shift and change.",
    ]
    
    COPING_SUGGESTIONS = [
        "Have you found anything that brings you even a small sense of comfort?",
        "What has helped you get through difficult times before?",
        "Is there anything that feels manageable for you right now?",
        "Sometimes focusing on just the next hour can help when everything feels overwhelming.",
        "What would taking care of yourself look like today?",
    ]
    
    QUESTION_STARTERS = [
        "Can you tell me more about",
        "What's it like when",
        "How long have you been feeling",
        "What do you think might help with",
        "When did you first notice",
    ]
    
    def __init__(self):
        self.usage_history = {}  # Track usage per session
    
    def get_varied_phrase(self, session_id: str, category: str, options: List[str]) -> str:
        """Get varied phrase avoiding recent usage"""
        key = f"{session_id}_{category}"
        
        # Get recent usage
        recent = self.usage_history.get(key, [])
        
        # Filter out recently used (last 2)
        available = [opt for opt in options if opt not in recent[-2:]]
        
        if not available:
            available = options
        
        # Select one
        selected = random.choice(available)
        
        # Update history
        recent.append(selected)
        self.usage_history[key] = recent[-3:]  # Keep last 3
        
        return selected


class EmotionalTrajectoryAnalyzer:
    """Analyzes emotional patterns for context-aware responses"""
    
    def analyze_trajectory(self, context_emotions: List[str]) -> Dict[str, any]:
        """Analyze emotional trajectory from context"""
        if not context_emotions:
            return {"state": "initial", "intensity": "normal"}
        
        # Count negative emotions
        negative_emotions = ["sadness", "fear", "anger", "disgust"]
        negative_count = sum(1 for e in context_emotions if e in negative_emotions)
        
        # Determine state
        if len(context_emotions) >= 3 and negative_count >= 3:
            state = "persistent_distress"
        elif len(context_emotions) >= 3 and len(set(context_emotions)) >= 3 and negative_count < 3:
            state = "fluctuating"
        elif len(set(context_emotions)) == 1 and context_emotions[0] in negative_emotions:
            state = "consistent_negative"
        else:
            state = "normal"
        
        # Determine intensity based on recent emotions
        recent_negative = sum(1 for e in context_emotions[-2:] if e in negative_emotions)
        if recent_negative >= 2:
            intensity = "high"
        elif recent_negative == 1:
            intensity = "moderate"
        else:
            intensity = "low"
        
        return {
            "state": state,
            "intensity": intensity,
            "negative_count": negative_count,
            "total_turns": len(context_emotions)
        }


class DepthDetector:
    """Detects emotional depth and intensity from text"""
    
    HIGH_INTENSITY_PATTERNS = [
        r"\b(no point|nothing matters|can't go on|give up|end it all)\b",
        r"\b(hopeless|worthless|meaningless|pointless)\b",
        r"\b(breaking|broken|shattered|destroyed)\b",
    ]
    
    MODERATE_INTENSITY_PATTERNS = [
        r"\b(can't take|can't handle|can't deal|too much)\b",
        r"\b(overwhelmed|exhausted|drained)\b",
    ]
    
    def detect_intensity(self, text: str) -> str:
        """Detect emotional intensity from text"""
        text_lower = text.lower()
        
        # Check high intensity patterns first
        for pattern in self.HIGH_INTENSITY_PATTERNS:
            if re.search(pattern, text_lower):
                return "high"
        
        # Check moderate intensity patterns
        for pattern in self.MODERATE_INTENSITY_PATTERNS:
            if re.search(pattern, text_lower):
                return "moderate"
        
        # Check for multiple negative indicators
        negative_indicators = ["can't", "won't", "never", "always", "nothing", "everything"]
        count = sum(1 for indicator in negative_indicators if indicator in text_lower)
        
        if count >= 2:
            return "moderate"
        
        return "normal"


class ProfessionalHelpGating:
    """Strict gating for professional help suggestions"""
    
    def should_suggest_professional_help(
        self,
        turn_number: int,
        trajectory: Dict[str, any],
        text_length: int,
        last_suggestion_turn: Optional[int] = None
    ) -> bool:
        """Determine if professional help should be suggested"""
        
        # Never suggest in early turns
        if turn_number < 4:
            return False
        
        # Never suggest for very short inputs
        if text_length < 20:  # Less than ~4 words
            return False
        
        # Never repeat suggestion in consecutive turns
        if last_suggestion_turn and (turn_number - last_suggestion_turn) < 3:
            return False
        
        # Only suggest for persistent distress
        if trajectory["state"] == "persistent_distress" and trajectory["negative_count"] >= 3:
            return True
        
        # Or for high intensity + multiple turns
        if turn_number >= 5 and trajectory["intensity"] == "high":
            return True
        
        return False


class AdvancedResponseBuilder:
    """Main advanced response builder"""
    
    def __init__(self):
        self.variation_engine = VariationEngine()
        self.trajectory_analyzer = EmotionalTrajectoryAnalyzer()
        self.depth_detector = DepthDetector()
        self.help_gating = ProfessionalHelpGating()
        self.session_data = {}  # Track per-session data
    
    def build_response(
        self,
        user_text: str,
        emotion: str,
        emotion_confidence: float,
        intent: str,
        turn_number: int,
        session_id: str,
        context_emotions: List[str] = None,
        base_template: str = ""
    ) -> str:
        """
        Build advanced, realistic response
        
        Args:
            user_text: Original user input
            emotion: Detected emotion
            emotion_confidence: Confidence score for emotion
            intent: Detected intent
            turn_number: Current turn number
            session_id: Session identifier
            context_emotions: List of recent emotions
            base_template: Base template (optional)
        
        Returns:
            Enhanced response string
        """
        # Initialize session data if needed
        if session_id not in self.session_data:
            self.session_data[session_id] = {
                "last_professional_suggestion": None,
                "mentioned_themes": set(),
                "response_flows_used": []
            }
        
        session_data = self.session_data[session_id]
        
        # Handle low confidence emotion
        if emotion_confidence < 0.75:
            emotion = "uncertain"
        
        # Analyze trajectory
        trajectory = self.trajectory_analyzer.analyze_trajectory(context_emotions or [])
        
        # Detect intensity
        intensity = self.depth_detector.detect_intensity(user_text)
        
        # Check if short input
        is_short_input = len(user_text.split()) <= 3
        
        # Build components
        components = self._build_components(
            user_text=user_text,
            emotion=emotion,
            intent=intent,
            turn_number=turn_number,
            session_id=session_id,
            trajectory=trajectory,
            intensity=intensity,
            is_short_input=is_short_input
        )
        
        # Select response flow
        flow = self._select_response_flow(
            session_id=session_id,
            turn_number=turn_number,
            intensity=intensity,
            is_short_input=is_short_input
        )
        
        # Assemble response
        response = self._assemble_response(components, flow)
        
        # Check for professional help suggestion
        should_suggest = self.help_gating.should_suggest_professional_help(
            turn_number=turn_number,
            trajectory=trajectory,
            text_length=len(user_text),
            last_suggestion_turn=session_data["last_professional_suggestion"]
        )
        
        if should_suggest:
            response += " Have you considered talking to a counselor or therapist about this?"
            session_data["last_professional_suggestion"] = turn_number
        
        return response
    
    def _build_components(
        self,
        user_text: str,
        emotion: str,
        intent: str,
        turn_number: int,
        session_id: str,
        trajectory: Dict,
        intensity: str,
        is_short_input: bool
    ) -> ResponseComponents:
        """Build response components"""
        
        # Validation (always present)
        if emotion == "uncertain":
            validation = "I may not be fully understanding, but it sounds like you're going through something difficult."
        elif intensity == "high":
            validation = self.variation_engine.get_varied_phrase(
                session_id, "validation_deep", 
                ["I can hear how much pain you're in.", "That sounds incredibly overwhelming.", "I sense how heavy this feels."]
            )
        else:
            validation = self.variation_engine.get_varied_phrase(
                session_id, "validation", self.variation_engine.VALIDATION_VARIANTS
            )
        
        # Reflection (if not short input)
        reflection = None
        if not is_short_input and turn_number <= 3:
            reflection_text = generate_reflection(user_text, emotion)
            if reflection_text:
                starter = self.variation_engine.get_varied_phrase(
                    session_id, "reflection_starter", self.variation_engine.REFLECTION_STARTERS
                )
                reflection = f"{starter} {reflection_text}."
        
        # Normalization (for persistent distress)
        normalization = None
        if trajectory["state"] == "persistent_distress":
            normalization = self.variation_engine.get_varied_phrase(
                session_id, "normalization", self.variation_engine.NORMALIZATION_PHRASES
            )
        
        # Coping (middle turns, not high intensity)
        coping = None
        if 2 <= turn_number <= 4 and intensity != "high" and not is_short_input:
            coping = self.variation_engine.get_varied_phrase(
                session_id, "coping", self.variation_engine.COPING_SUGGESTIONS
            )
        
        # Gentle guidance (for high intensity or later turns)
        gentle_guidance = None
        if intensity == "high" or turn_number >= 4:
            gentle_guidance = self.variation_engine.get_varied_phrase(
                session_id, "guidance", self.variation_engine.GENTLE_GUIDANCE
            )
        
        # Question (always present, adapted to context)
        if is_short_input:
            question = self._build_clarification_question(user_text, emotion)
        else:
            question = self._build_contextual_question(intent, intensity, turn_number)
        
        return ResponseComponents(
            validation=validation,
            reflection=reflection,
            normalization=normalization,
            coping=coping,
            gentle_guidance=gentle_guidance,
            question=question
        )
    
    def _select_response_flow(
        self,
        session_id: str,
        turn_number: int,
        intensity: str,
        is_short_input: bool
    ) -> str:
        """Select response flow avoiding repetition"""
        
        session_data = self.session_data[session_id]
        
        if is_short_input:
            return "validation_question"
        
        # Available flows
        flows = [
            "validation_reflection_question",
            "validation_reflection_coping_question", 
            "reflection_normalization_question",
            "validation_guidance_question",
            "validation_normalization_guidance_question"
        ]
        
        # Filter out recently used flows
        recent_flows = session_data["response_flows_used"][-2:]
        available_flows = [f for f in flows if f not in recent_flows]
        
        if not available_flows:
            available_flows = flows
        
        # Select based on context
        if intensity == "high":
            preferred = [f for f in available_flows if "guidance" in f or "normalization" in f]
            if preferred:
                available_flows = preferred
        
        selected = random.choice(available_flows)
        
        # Update history
        recent_flows.append(selected)
        session_data["response_flows_used"] = recent_flows[-3:]
        
        return selected
    
    def _assemble_response(self, components: ResponseComponents, flow: str) -> str:
        """Assemble response based on selected flow"""
        parts = []
        
        if flow == "validation_question":
            parts = [components.validation, components.question]
        
        elif flow == "validation_reflection_question":
            parts = [components.validation]
            if components.reflection:
                parts.append(components.reflection)
            parts.append(components.question)
        
        elif flow == "validation_reflection_coping_question":
            parts = [components.validation]
            if components.reflection:
                parts.append(components.reflection)
            if components.coping:
                parts.append(components.coping)
            parts.append(components.question)
        
        elif flow == "reflection_normalization_question":
            if components.reflection:
                parts.append(components.reflection)
            if components.normalization:
                parts.append(components.normalization)
            parts.append(components.question)
        
        elif flow == "validation_guidance_question":
            parts = [components.validation]
            if components.gentle_guidance:
                parts.append(components.gentle_guidance)
            parts.append(components.question)
        
        elif flow == "validation_normalization_guidance_question":
            parts = [components.validation]
            if components.normalization:
                parts.append(components.normalization)
            if components.gentle_guidance:
                parts.append(components.gentle_guidance)
            parts.append(components.question)
        
        # Filter out None values and join
        parts = [p for p in parts if p]
        return " ".join(parts)
    
    def _build_clarification_question(self, user_text: str, emotion: str) -> str:
        """Build clarification question for short inputs"""
        text_lower = user_text.lower().strip()
        
        if "tired" in text_lower:
            return "Do you feel physically tired, or more mentally exhausted?"
        elif "sad" in text_lower:
            return "What's been making you feel this way?"
        elif "angry" in text_lower or "mad" in text_lower:
            return "What's been frustrating you?"
        elif "anxious" in text_lower or "worried" in text_lower:
            return "What's been on your mind?"
        elif "stressed" in text_lower:
            return "What's been creating stress for you?"
        else:
            return "Can you tell me a bit more about what's going on?"
    
    def _build_contextual_question(self, intent: str, intensity: str, turn_number: int) -> str:
        """Build contextual question based on intent and context"""
        
        if intensity == "high":
            questions = [
                "What would help you feel even a little bit safer right now?",
                "Is there anyone in your life you feel you could reach out to?",
                "What has helped you get through really difficult times before?",
            ]
        elif intent == "anxiety and panic":
            questions = [
                "When do you notice these feelings are strongest?",
                "What thoughts tend to go through your mind when you feel this way?",
                "Have you noticed anything that helps calm these feelings?",
            ]
        elif intent == "sadness and depression":
            questions = [
                "How long have you been carrying this feeling?",
                "What does a typical day look like for you right now?",
                "Is there anything that brings you even small moments of comfort?",
            ]
        elif intent == "loneliness and isolation":
            questions = [
                "What does connection mean to you?",
                "When did you last feel truly understood by someone?",
                "What makes it hard to reach out to others?",
            ]
        else:
            questions = [
                "What's been the hardest part about this?",
                "How has this been affecting your daily life?",
                "What would feeling better look like to you?",
            ]
        
        return random.choice(questions)
    
    def clear_session(self, session_id: str):
        """Clear session data"""
        if session_id in self.session_data:
            del self.session_data[session_id]


# Singleton instance
_advanced_builder: Optional[AdvancedResponseBuilder] = None


def get_advanced_response_builder() -> AdvancedResponseBuilder:
    """Get singleton advanced response builder"""
    global _advanced_builder
    if _advanced_builder is None:
        _advanced_builder = AdvancedResponseBuilder()
    return _advanced_builder