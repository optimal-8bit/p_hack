"""
Structured Payload Builder for LLM Generation
Constructs the structured data payload that controls LLM output
"""

import logging
from typing import Dict, List, Optional
from pipeline.context_tracker import TurnRecord

logger = logging.getLogger(__name__)


class PayloadBuilder:
    """Builds structured payload for controlled LLM generation"""
    
    def build_llm_payload(
        self,
        user_input: str,
        processed_text: str,
        message_type: Dict,
        emotion: str,
        emotion_confidence: float,
        intent: str,
        intent_confidence: float,
        turn_number: int,
        context: List[TurnRecord],
        response_components: Dict,
        allow_therapist: bool = False,
        facial_emotion_data: Optional[dict] = None
    ) -> Dict:
        """
        Build structured payload for therapeutic LLM generation
        
        Args:
            user_input: Original user message
            processed_text: Cleaned/translated text
            message_type: Message type detection result
            emotion: Detected emotion
            emotion_confidence: Emotion confidence score
            intent: Detected intent
            intent_confidence: Intent confidence score
            turn_number: Current turn number
            context: Conversation context
            response_components: Generated response components
            allow_therapist: Whether therapist suggestion is allowed
            
        Returns:
            Structured payload dict for therapeutic LLM
        """
        
        # Extract context information
        context_info = self._extract_context_info(context)
        
        # Determine therapeutic strategy
        therapeutic_strategy = self._determine_therapeutic_strategy(
            message_type, emotion, emotion_confidence, intent, turn_number, context
        )
        
        # Build therapeutic intervention plan
        intervention_plan = self._build_therapeutic_plan(
            emotion, intent, response_components, context_info
        )
        
        # Construct therapeutic payload
        payload = {
            "user_input": user_input,
            "processed_text": processed_text,
            "emotion": emotion,
            "intent": intent,
            "context": context_info,
            "therapeutic_strategy": therapeutic_strategy,
            "intervention_plan": intervention_plan,
            "session_info": {
                "turn_number": turn_number,
                "session_stage": self._determine_session_stage(turn_number, context),
                "therapeutic_alliance": self._assess_alliance(context),
                "client_readiness": self._assess_readiness(emotion, intent, context)
            },
            "multimodal_data": {
                "has_facial_emotion": facial_emotion_data is not None,
                "facial_emotion": facial_emotion_data.get("dominant_emotion") if facial_emotion_data else None,
                "facial_confidence": facial_emotion_data.get("confidence") if facial_emotion_data else None,
                "age": facial_emotion_data.get("age") if facial_emotion_data else None,
                "gender": facial_emotion_data.get("gender") if facial_emotion_data else None
            } if facial_emotion_data else None,
            "constraints": {
                "max_sentences": 6,  # Allow more depth for therapeutic responses
                "style": "professional, warm, therapeutic",
                "approach": "evidence-based",
                "maintain_boundaries": True,
                "encourage_exploration": True
            }
        }
        
        logger.debug(f"Built therapeutic LLM payload for {emotion}/{intent} (multimodal: {facial_emotion_data is not None})")
        return payload
    
    def _extract_context_info(self, context: List[TurnRecord]) -> Dict:
        """Extract relevant context information"""
        if not context:
            return {
                "turn_number": 1,
                "dominant_emotion": None,
                "previous_emotions": [],
                "recent_messages": [],
                "topics": []
            }
        
        # Get recent emotions (last 3 turns)
        recent_emotions = [turn.emotion for turn in context[-3:]]
        
        # Get dominant emotion
        emotion_counts = {}
        for turn in context:
            emotion_counts[turn.emotion] = emotion_counts.get(turn.emotion, 0) + 1
        dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else None
        
        # Get recent messages (last 2 turns, user text only)
        recent_messages = [turn.user_text for turn in context[-2:]]
        
        # Extract basic topics (simple keyword extraction)
        topics = self._extract_topics(context)
        
        return {
            "turn_number": len(context) + 1,
            "dominant_emotion": dominant_emotion,
            "previous_emotions": recent_emotions,
            "recent_messages": recent_messages,
            "topics": topics
        }
    
    def _extract_topics(self, context: List[TurnRecord]) -> List[str]:
        """Extract mentioned topics from conversation"""
        topics = set()
        
        # Common topic keywords
        topic_keywords = {
            "work": ["work", "job", "career", "office", "boss", "colleague"],
            "school": ["school", "exam", "test", "study", "homework", "class"],
            "family": ["family", "parent", "mother", "father", "sibling", "child"],
            "relationship": ["relationship", "partner", "boyfriend", "girlfriend", "marriage"],
            "health": ["health", "sick", "pain", "doctor", "hospital", "medical"],
            "money": ["money", "financial", "debt", "bills", "income", "budget"]
        }
        
        # Check last 3 messages for topics
        recent_text = " ".join([turn.user_text.lower() for turn in context[-3:]])
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in recent_text for keyword in keywords):
                topics.add(topic)
        
        return list(topics)[:3]  # Limit to 3 topics
    
    def _determine_therapeutic_strategy(
        self,
        message_type: Dict,
        emotion: str,
        emotion_confidence: float,
        intent: str,
        turn_number: int,
        context: List[TurnRecord]
    ) -> Dict:
        """Determine therapeutic intervention strategy"""
        
        # Map emotions to therapeutic approaches
        emotion_strategies = {
            "sadness": ["validation", "cognitive_reframe", "behavioral_activation"],
            "anxiety": ["grounding", "cognitive_restructuring", "exposure_preparation"],
            "anger": ["validation", "emotion_regulation", "perspective_taking"],
            "fear": ["safety_assessment", "gradual_exposure", "coping_skills"],
            "joy": ["amplification", "meaning_making", "strength_building"],
            "disgust": ["acceptance", "values_clarification", "boundary_setting"],
            "surprise": ["processing", "integration", "adaptive_response"]
        }
        
        # Map intents to therapeutic focus
        intent_focus = {
            "anxiety and panic": "anxiety_management",
            "depression and sadness": "depression_treatment", 
            "relationship issues": "interpersonal_therapy",
            "work stress": "stress_management",
            "trauma and grief": "trauma_informed_care",
            "self-esteem": "self_compassion_building",
            "general emotional support": "supportive_therapy"
        }
        
        # Determine primary therapeutic modality
        if emotion in ["anxiety", "fear"] or "anxiety" in intent:
            modality = "CBT"  # Cognitive Behavioral Therapy
        elif emotion == "sadness" or "depression" in intent:
            modality = "CBT_IPT"  # CBT + Interpersonal Therapy
        elif "relationship" in intent:
            modality = "IPT"  # Interpersonal Therapy
        elif "trauma" in intent:
            modality = "TF_CBT"  # Trauma-Focused CBT
        else:
            modality = "Person_Centered"  # Person-Centered Therapy
        
        return {
            "primary_modality": modality,
            "techniques": emotion_strategies.get(emotion, ["validation", "exploration"]),
            "therapeutic_focus": intent_focus.get(intent, "supportive_therapy"),
            "session_goals": self._determine_session_goals(emotion, intent, turn_number),
            "intervention_level": self._determine_intervention_level(emotion_confidence, turn_number)
        }
    
    def _determine_session_goals(self, emotion: str, intent: str, turn_number: int) -> List[str]:
        """Determine therapeutic goals for this session"""
        goals = []
        
        # Early session goals (turns 1-3)
        if turn_number <= 3:
            goals.extend(["build_rapport", "assess_needs", "normalize_experience"])
        
        # Emotion-specific goals
        if emotion in ["sadness", "depression"]:
            goals.extend(["identify_triggers", "challenge_negative_thoughts", "behavioral_activation"])
        elif emotion in ["anxiety", "fear"]:
            goals.extend(["anxiety_psychoeducation", "coping_skills", "gradual_exposure"])
        elif emotion == "anger":
            goals.extend(["anger_management", "communication_skills", "trigger_identification"])
        
        # Intent-specific goals
        if "relationship" in intent:
            goals.extend(["communication_patterns", "boundary_setting", "conflict_resolution"])
        elif "work" in intent:
            goals.extend(["stress_management", "work_life_balance", "assertiveness"])
        
        return goals[:3]  # Limit to 3 main goals
    
    def _determine_intervention_level(self, emotion_confidence: float, turn_number: int) -> str:
        """Determine appropriate intervention intensity"""
        if emotion_confidence > 0.8 and turn_number > 3:
            return "intensive"  # High confidence, established rapport
        elif emotion_confidence > 0.6:
            return "moderate"   # Good confidence
        else:
            return "gentle"     # Low confidence, be more careful
    
    def _build_therapeutic_plan(
        self, 
        emotion: str, 
        intent: str, 
        components: Dict, 
        context_info: Dict
    ) -> Dict:
        """Build therapeutic intervention plan"""
        
        # Core therapeutic components
        plan = {
            "validation": self._create_validation(emotion, intent),
            "psychoeducation": self._create_psychoeducation(emotion, intent),
            "intervention": self._create_intervention(emotion, intent, context_info),
            "exploration": self._create_exploration_question(emotion, intent),
            "homework": self._create_therapeutic_homework(emotion, intent)
        }
        
        return plan
    
    def _create_validation(self, emotion: str, intent: str) -> str:
        """Create emotion validation statement"""
        validations = {
            "sadness": "It takes courage to share these difficult feelings, and what you're experiencing is completely understandable.",
            "anxiety": "Anxiety can feel overwhelming, and it's natural to seek ways to manage these intense feelings.",
            "anger": "Your anger makes sense given what you're going through, and it's important we explore what's underneath it.",
            "fear": "Fear is a normal response to uncertainty, and acknowledging it is the first step toward managing it.",
            "joy": "It's wonderful that you're experiencing positive emotions - let's explore what's contributing to this.",
        }
        return validations.get(emotion, "Your feelings are valid and it's important that we explore them together.")
    
    def _create_psychoeducation(self, emotion: str, intent: str) -> str:
        """Create brief psychoeducational component"""
        education = {
            "anxiety": "Anxiety often involves our mind's attempt to protect us by anticipating threats, but sometimes this system becomes overactive.",
            "sadness": "Sadness is a natural emotional response that signals something important to us has been affected or lost.",
            "anger": "Anger often serves as a secondary emotion, sometimes protecting us from more vulnerable feelings underneath.",
        }
        return education.get(emotion, "Understanding our emotions helps us respond to them more effectively.")
    
    def _create_intervention(self, emotion: str, intent: str, context_info: Dict) -> str:
        """Create therapeutic intervention"""
        interventions = {
            "anxiety": "Let's try a grounding technique: notice 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
            "sadness": "When we're feeling low, small behavioral changes can help. What's one small thing you could do today that usually brings you some comfort?",
            "anger": "Let's pause and notice where you feel this anger in your body. Sometimes our physical sensations give us important information.",
        }
        return interventions.get(emotion, "What coping strategies have you found helpful in the past when dealing with similar situations?")
    
    def _create_exploration_question(self, emotion: str, intent: str) -> str:
        """Create therapeutic exploration question"""
        questions = {
            "anxiety": "What thoughts tend to go through your mind when the anxiety is at its strongest?",
            "sadness": "When you think about this situation, what feels most difficult or painful about it?",
            "anger": "What do you think might be underneath this anger - what other feelings might be there?",
            "relationship": "How do you think this pattern might be affecting your relationships with others?",
        }
        
        key = emotion if emotion in questions else intent.split()[0] if intent else "general"
        return questions.get(key, "What would it look like if this situation improved? What would be different?")
    
    def _create_therapeutic_homework(self, emotion: str, intent: str) -> str:
        """Create therapeutic homework/practice suggestion"""
        homework = {
            "anxiety": "Consider keeping a brief anxiety log this week - noting triggers, thoughts, and what helps.",
            "sadness": "Try to engage in one small pleasant activity each day, even if you don't feel like it initially.",
            "anger": "Practice the pause technique when you notice anger rising - take three deep breaths before responding.",
        }
        return homework.get(emotion, "Reflect on our conversation and notice what resonates most with you.")
    
    def _determine_session_stage(self, turn_number: int, context: List[TurnRecord]) -> str:
        """Determine what stage of therapy this represents"""
        if turn_number <= 2:
            return "initial_assessment"
        elif turn_number <= 5:
            return "rapport_building"
        elif turn_number <= 10:
            return "active_intervention"
        else:
            return "maintenance_integration"
    
    def _assess_alliance(self, context: List[TurnRecord]) -> str:
        """Assess therapeutic alliance strength"""
        if len(context) < 2:
            return "building"
        elif len(context) < 5:
            return "developing"
        else:
            return "established"
    
    def _assess_readiness(self, emotion: str, intent: str, context: List[TurnRecord]) -> str:
        """Assess client readiness for change"""
        # Simple heuristic based on engagement
        if len(context) > 3:
            return "action_oriented"
        elif emotion in ["anxiety", "sadness"] and len(context) > 1:
            return "contemplative"
        else:
            return "pre_contemplative"


# Singleton instance
_payload_builder: Optional[PayloadBuilder] = None


def get_payload_builder() -> PayloadBuilder:
    """Get singleton payload builder instance"""
    global _payload_builder
    if _payload_builder is None:
        _payload_builder = PayloadBuilder()
    return _payload_builder