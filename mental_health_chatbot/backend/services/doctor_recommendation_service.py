"""Service for generating doctor recommendations based on chat analysis"""
import logging
from typing import Dict, List, Optional
from database.doctor_models import DoctorRecommendation, Doctor
from database.db import get_db_session

logger = logging.getLogger(__name__)


class DoctorRecommendationService:
    """Analyzes chat context and generates doctor recommendations"""
    
    # Symptom patterns that suggest professional help
    SYMPTOM_PATTERNS = {
        "psychiatrist": [
            "suicidal", "suicide", "kill myself", "end my life",
            "severe depression", "can't get out of bed", "no reason to live",
            "hearing voices", "hallucination", "paranoid", "delusion",
            "bipolar", "manic", "psychotic"
        ],
        "psychologist": [
            "anxiety", "panic attack", "worried", "stress", "overwhelmed",
            "trauma", "ptsd", "abuse", "grief", "loss", "depression",
            "relationship problems", "family issues", "anger management",
            "anxious", "panic", "fear", "scared", "nervous", "tense",
            "depressed", "sad", "hopeless", "worthless", "empty",
            "can't cope", "struggling", "suffering", "pain", "hurt"
        ],
        "therapist": [
            "talk to someone", "need help", "counseling", "therapy",
            "mental health", "emotional support", "coping", "struggling",
            "need someone", "want to talk", "feeling alone", "isolated",
            "relationship", "marriage", "family", "work stress"
        ],
        "general_practitioner": [
            "sleep problems", "insomnia", "fatigue", "tired",
            "headache", "physical symptoms", "medication", "prescription",
            "can't sleep", "exhausted", "no energy", "always tired"
        ]
    }
    
    # Emotion patterns that suggest urgency
    URGENCY_EMOTIONS = {
        "urgent": ["suicidal", "severe_distress", "panic"],
        "high": ["anxiety", "fear", "anger", "sadness"],
        "normal": ["worried", "stressed", "confused"],
        "low": ["neutral", "calm"]
    }
    
    def __init__(self):
        self.recommendation_threshold = 2  # Lower threshold for easier testing (was 3)
    
    def analyze_conversation(
        self,
        session_id: str,
        messages: List[Dict],
        emotions: List[str],
        intents: List[str],
        is_crisis: bool = False
    ) -> Optional[Dict]:
        """
        Analyze conversation and determine if doctor recommendation is needed
        
        Args:
            session_id: Chat session ID
            messages: List of user messages
            emotions: List of detected emotions
            intents: List of detected intents
            is_crisis: Whether crisis was detected
            
        Returns:
            Recommendation dict or None if no recommendation needed
        """
        try:
            # Combine all text for analysis
            full_text = " ".join([msg.get("content", "").lower() for msg in messages])
            
            # Detect symptoms and specializations
            detected_symptoms = []
            specialization_scores = {}
            
            for specialization, patterns in self.SYMPTOM_PATTERNS.items():
                score = 0
                for pattern in patterns:
                    if pattern in full_text:
                        score += 1
                        detected_symptoms.append(pattern)
                
                if score > 0:
                    specialization_scores[specialization] = score
            
            # Determine urgency based on emotions and crisis flag
            urgency = self._determine_urgency(emotions, is_crisis)
            
            # Check if recommendation is needed
            if is_crisis or len(detected_symptoms) >= self.recommendation_threshold:
                # Get top specialization
                if specialization_scores:
                    recommended_specialization = max(
                        specialization_scores.items(),
                        key=lambda x: x[1]
                    )[0]
                else:
                    recommended_specialization = "psychologist"  # Default
                
                # Generate reason
                reason = self._generate_reason(
                    detected_symptoms,
                    emotions,
                    is_crisis
                )
                
                return {
                    "session_id": session_id,
                    "recommended_specialization": recommended_specialization,
                    "reason": reason,
                    "urgency": urgency,
                    "symptoms": list(set(detected_symptoms)),
                    "is_crisis": is_crisis,
                    "emotion_context": {
                        "emotions": emotions,
                        "intents": intents
                    }
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing conversation: {e}", exc_info=True)
            return None
    
    def _determine_urgency(self, emotions: List[str], is_crisis: bool) -> str:
        """Determine urgency level based on emotions and crisis flag"""
        if is_crisis:
            return "urgent"
        
        for emotion in emotions:
            for urgency_level, urgency_emotions in self.URGENCY_EMOTIONS.items():
                if emotion.lower() in urgency_emotions:
                    return urgency_level
        
        return "normal"
    
    def _generate_reason(
        self,
        symptoms: List[str],
        emotions: List[str],
        is_crisis: bool
    ) -> str:
        """Generate human-readable reason for recommendation"""
        if is_crisis:
            return (
                "Based on our conversation, I'm concerned about your wellbeing. "
                "I strongly recommend speaking with a mental health professional "
                "who can provide immediate support and guidance."
            )
        
        if len(symptoms) > 5:
            return (
                "You've mentioned several concerning symptoms during our conversation. "
                "A mental health professional can provide personalized support and "
                "treatment options that may help you feel better."
            )
        
        if "anxiety" in emotions or "fear" in emotions:
            return (
                "It sounds like you're experiencing significant anxiety. "
                "A therapist can help you develop coping strategies and work through "
                "these feelings in a supportive environment."
            )
        
        if "sadness" in emotions or "depression" in [s for s in symptoms]:
            return (
                "You seem to be going through a difficult time. "
                "Speaking with a mental health professional can provide valuable "
                "support and help you develop strategies to feel better."
            )
        
        return (
            "Based on what you've shared, I think speaking with a mental health "
            "professional could be beneficial. They can provide personalized guidance "
            "and support tailored to your specific situation."
        )
    
    async def save_recommendation(self, recommendation_data: Dict) -> Optional[str]:
        """Save recommendation to database"""
        try:
            from database.db import async_session_factory
            from sqlalchemy import select
            
            async with async_session_factory() as db:
                # Get recommended doctors
                specialization = recommendation_data.get("recommended_specialization")
                
                recommended_doctors = []
                if specialization:
                    result = await db.execute(
                        select(Doctor).filter(
                            Doctor.specialization == specialization,
                            Doctor.is_active == True
                        ).order_by(Doctor.rating.desc()).limit(3)
                    )
                    doctors = result.scalars().all()
                    recommended_doctors = [doc.id for doc in doctors]
                
                # Create recommendation
                recommendation = DoctorRecommendation(
                    session_id=recommendation_data["session_id"],
                    recommended_specialization=specialization,
                    reason=recommendation_data["reason"],
                    urgency=recommendation_data["urgency"],
                    symptoms=recommendation_data.get("symptoms", []),
                    emotion_context=recommendation_data.get("emotion_context", {}),
                    recommended_doctors=recommended_doctors,
                    is_crisis=recommendation_data.get("is_crisis", False)
                )
                
                db.add(recommendation)
                await db.commit()
                await db.refresh(recommendation)
                
                logger.info(
                    f"✅ Saved doctor recommendation for session {recommendation_data['session_id']}: "
                    f"{specialization} (urgency: {recommendation_data['urgency']})"
                )
                
                return recommendation.id
                
        except Exception as e:
            logger.error(f"Error saving recommendation: {e}", exc_info=True)
            return None
    
    def should_show_recommendation(
        self,
        turn_number: int,
        has_existing_recommendation: bool
    ) -> bool:
        """Determine if recommendation should be shown in response"""
        # Show recommendation after a few turns, but not repeatedly
        if has_existing_recommendation:
            return False
        
        # Show after 2+ turns if symptoms detected (lowered from 3 for easier testing)
        return turn_number >= 2


# Singleton instance
_recommendation_service = None


def get_recommendation_service() -> DoctorRecommendationService:
    """Get singleton recommendation service instance"""
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = DoctorRecommendationService()
    return _recommendation_service
