"""
FORCE DOCTOR RECOMMENDATIONS TO WORK
This script will make recommendations appear on EVERY message for testing
"""

# Backup the original recommendation service
import shutil
import os

# Create backup
original_file = "services/doctor_recommendation_service.py"
backup_file = "services/doctor_recommendation_service_backup.py"

if os.path.exists(original_file):
    shutil.copy(original_file, backup_file)
    print(f"✅ Backed up original to {backup_file}")

# Create a FORCED version that ALWAYS returns recommendations
forced_service = '''"""Service for generating doctor recommendations based on chat analysis - FORCED VERSION"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DoctorRecommendationService:
    """Analyzes chat context and generates doctor recommendations - FORCED TO ALWAYS RECOMMEND"""
    
    def __init__(self):
        self.recommendation_threshold = 1  # FORCE: Always recommend after 1 message
    
    def analyze_conversation(
        self,
        session_id: str,
        messages: List[Dict],
        emotions: List[str],
        intents: List[str],
        is_crisis: bool = False
    ) -> Optional[Dict]:
        """
        FORCED VERSION: ALWAYS returns a recommendation
        """
        try:
            print(f"🔥 FORCED RECOMMENDATION for session {session_id}")
            
            # ALWAYS return a recommendation regardless of content
            if is_crisis:
                return {
                    "session_id": session_id,
                    "recommended_specialization": "psychiatrist",
                    "reason": "CRISIS DETECTED: I'm concerned about your wellbeing. I strongly recommend speaking with a mental health professional immediately.",
                    "urgency": "urgent",
                    "symptoms": ["crisis"],
                    "is_crisis": True,
                    "emotion_context": {
                        "emotions": emotions,
                        "intents": intents
                    }
                }
            
            # For any other message, recommend psychologist
            return {
                "session_id": session_id,
                "recommended_specialization": "psychologist",
                "reason": "Based on our conversation, I think speaking with a mental health professional could be beneficial. They can provide personalized support and guidance.",
                "urgency": "normal",
                "symptoms": ["general_concern"],
                "is_crisis": False,
                "emotion_context": {
                    "emotions": emotions,
                    "intents": intents
                }
            }
            
        except Exception as e:
            logger.error(f"Error in FORCED recommendation: {e}", exc_info=True)
            # Even if there's an error, return a recommendation
            return {
                "session_id": session_id,
                "recommended_specialization": "psychologist",
                "reason": "I think it would be helpful to speak with a mental health professional.",
                "urgency": "normal",
                "symptoms": ["general"],
                "is_crisis": False,
                "emotion_context": {"emotions": emotions, "intents": intents}
            }
    
    async def save_recommendation(self, recommendation_data: Dict) -> Optional[str]:
        """Save recommendation to database"""
        try:
            # Import here to avoid circular imports
            from database.db import async_session_factory
            from database.doctor_models import DoctorRecommendation, Doctor
            
            async with async_session_factory() as db:
                # Get recommended doctors
                specialization = recommendation_data.get("recommended_specialization")
                
                recommended_doctors = []
                if specialization:
                    from sqlalchemy import and_
                    doctors = db.query(Doctor).filter(
                        and_(
                            Doctor.specialization == specialization,
                            Doctor.is_active == True
                        )
                    ).order_by(Doctor.rating.desc()).limit(3).all()
                    
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
                
                logger.info(f"✅ FORCED: Saved recommendation for session {recommendation_data['session_id']}")
                return recommendation.id
                
        except Exception as e:
            logger.error(f"Error saving FORCED recommendation: {e}", exc_info=True)
            return None
    
    def should_show_recommendation(
        self,
        turn_number: int,
        has_existing_recommendation: bool
    ) -> bool:
        """FORCED VERSION: ALWAYS show recommendation"""
        return True  # ALWAYS show recommendations


# Singleton instance
_recommendation_service = None


def get_recommendation_service() -> DoctorRecommendationService:
    """Get singleton recommendation service instance"""
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = DoctorRecommendationService()
    return _recommendation_service
'''

# Write the forced version
with open(original_file, 'w') as f:
    f.write(forced_service)

print("🔥 FORCED RECOMMENDATIONS ACTIVATED!")
print("📝 Every message will now generate a doctor recommendation")
print("🔄 Restart your backend: python main.py")
print("💬 Test any message in chat - recommendation will appear!")
print("")
print("⚠️  To restore original behavior later:")
print(f"   cp {backup_file} {original_file}")