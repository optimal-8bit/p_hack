"""
Health service layer for diagnosis and health checks.
"""
import base64
import logging
from typing import List, Optional

from app.core.database import get_database
from app.core.sqlite_db import save_diagnosis, get_diagnosis_history
from app.modules.health.ai_engine import analyze_image
from app.modules.health.symptom_analyzer import analyze_symptoms
from app.modules.health.decision_engine import (
    combine_scores,
    get_top_prediction,
    calculate_risk_level,
    generate_explanation
)

logger = logging.getLogger(__name__)


async def health_status() -> dict[str, str]:
    """Check system health status."""
    try:
        db = get_database()
        await db.command("ping")
        return {"status": "ok", "mongo": "connected"}
    except Exception:
        return {"status": "degraded", "mongo": "disconnected"}


async def analyze_patient(
    symptoms: List[str],
    image_base64: Optional[str] = None
) -> dict:
    """
    Analyze patient symptoms and image to provide diagnosis.
    
    Args:
        symptoms: List of symptom names
        image_base64: Optional base64-encoded image
        
    Returns:
        Dictionary containing diagnosis results
    """
    logger.info(f"Starting diagnosis analysis with {len(symptoms)} symptoms")
    
    # Step 1: Analyze symptoms
    symptom_scores = analyze_symptoms(symptoms)
    logger.info(f"Symptom analysis complete: {symptom_scores}")
    
    # Step 2: Analyze image if provided
    image_scores = {}
    has_image = False
    
    if image_base64:
        try:
            # Decode base64 image
            # Remove data URL prefix if present
            if "," in image_base64:
                image_base64 = image_base64.split(",", 1)[1]
            
            image_bytes = base64.b64decode(image_base64)
            has_image = True
            
            # Run image analysis
            image_scores = analyze_image(image_bytes)
            logger.info(f"Image analysis complete: {image_scores}")
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            # Continue without image analysis
            has_image = False
    
    # Step 3: Combine scores
    if has_image and image_scores:
        # Use both image and symptom scores
        combined_scores = combine_scores(image_scores, symptom_scores)
    elif has_image:
        # Image analysis failed, use only symptoms
        combined_scores = symptom_scores
    else:
        # No image provided, use only symptoms
        combined_scores = symptom_scores
    
    logger.info(f"Combined scores: {combined_scores}")
    
    # Step 4: Get top prediction
    disease, confidence = get_top_prediction(combined_scores)
    
    # Step 5: Calculate risk level
    risk_level = calculate_risk_level(confidence)
    
    # Step 6: Generate explanation
    explanation = generate_explanation(disease, confidence, symptoms, has_image)
    
    # Step 7: Save to database
    try:
        symptoms_str = ", ".join(symptoms) if symptoms else "none"
        save_diagnosis(
            symptoms=symptoms_str,
            prediction=disease,
            confidence=confidence,
            risk_level=risk_level,
            explanation=explanation,
            image_path="base64_image" if has_image else None
        )
        logger.info("Diagnosis saved to database")
    except Exception as e:
        logger.error(f"Error saving diagnosis to database: {e}")
    
    # Return results
    return {
        "disease": disease,
        "confidence": confidence,
        "risk_level": risk_level,
        "explanation": explanation,
        "all_scores": combined_scores
    }


async def get_history(limit: int = 10) -> dict:
    """
    Get diagnosis history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        Dictionary containing history records
    """
    try:
        history = get_diagnosis_history(limit)
        return {
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Error retrieving diagnosis history: {e}")
        return {
            "history": [],
            "count": 0
        }
