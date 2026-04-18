"""
Decision engine that combines image analysis and symptom analysis.
Implements deterministic rule-based disease prediction.
"""
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

# All possible diseases
DISEASES = [
    "fungal infection",
    "eczema",
    "psoriasis",
    "bacterial infection"
]


def combine_scores(
    image_scores: Dict[str, float],
    symptom_scores: Dict[str, float],
    image_weight: float = 0.7,
    symptom_weight: float = 0.3
) -> Dict[str, float]:
    """
    Combine image and symptom scores with weighted average.
    Image analysis is weighted higher (70%) as it provides visual evidence.
    
    Args:
        image_scores: Disease probabilities from image analysis (0-1)
        symptom_scores: Disease probabilities from symptom analysis (0-1)
        image_weight: Weight for image scores (default 0.7)
        symptom_weight: Weight for symptom scores (default 0.3)
        
    Returns:
        Combined disease probabilities (normalized to sum to 1.0)
    """
    combined_scores: Dict[str, float] = {}
    
    # Get all diseases from both sources
    all_diseases = set(image_scores.keys()) | set(symptom_scores.keys())
    
    # Combine scores with weighted average
    for disease in all_diseases:
        image_score = image_scores.get(disease, 0.0)
        symptom_score = symptom_scores.get(disease, 0.0)
        
        combined_score = (image_score * image_weight) + (symptom_score * symptom_weight)
        combined_scores[disease] = combined_score
    
    # Normalize to sum to 1.0 for consistency
    total = sum(combined_scores.values())
    if total > 0:
        combined_scores = {
            disease: score / total
            for disease, score in combined_scores.items()
        }
    
    logger.info(f"Combined scores (img:{image_weight}, sym:{symptom_weight}): {combined_scores}")
    return combined_scores


def get_top_prediction(scores: Dict[str, float]) -> Tuple[str, float]:
    """
    Get the disease with highest score.
    
    Args:
        scores: Disease probabilities
        
    Returns:
        Tuple of (disease_name, confidence_score)
    """
    if not scores:
        return ("unknown", 0.0)
    
    top_disease = max(scores.items(), key=lambda x: x[1])
    return top_disease


def calculate_risk_level(confidence: float) -> str:
    """
    Calculate risk level based on confidence score.
    
    Args:
        confidence: Confidence score (0-1)
        
    Returns:
        Risk level: "High", "Medium", or "Low"
    """
    if confidence >= 0.75:
        return "High"
    elif confidence >= 0.4:
        return "Medium"
    else:
        return "Low"


def generate_explanation(
    disease: str,
    confidence: float,
    symptoms: List[str],
    has_image: bool
) -> str:
    """
    Generate human-readable explanation for the diagnosis.
    Provides context about detection method, symptoms, and confidence level.
    
    Args:
        disease: Predicted disease name
        confidence: Confidence score (0-1)
        symptoms: List of symptoms provided
        has_image: Whether image was analyzed
        
    Returns:
        Explanation text
    """
    explanation_parts = []
    
    # Base explanation with detection method
    if has_image and symptoms:
        explanation_parts.append(
            f"Based on visual pattern analysis and reported symptoms ({', '.join(symptoms)}), "
            f"the system detected indicators consistent with {disease}."
        )
    elif has_image:
        explanation_parts.append(
            f"Based on visual pattern analysis of the provided image, "
            f"the system detected patterns consistent with {disease}."
        )
    elif symptoms:
        symptom_text = ", ".join(symptoms)
        explanation_parts.append(
            f"Based on the reported symptoms ({symptom_text}), "
            f"the analysis suggests {disease}."
        )
    else:
        explanation_parts.append(
            f"The system predicts {disease}."
        )
    
    # Add disease-specific context
    disease_context = {
        "fungal infection": "Fungal infections typically present with itching and distinctive visual patterns.",
        "eczema": "Eczema often shows redness and inflammation with associated itching.",
        "psoriasis": "Psoriasis commonly presents with scaly patches and may cause fatigue.",
        "bacterial infection": "Bacterial infections may present with fever, redness, and systemic symptoms."
    }
    
    if disease in disease_context:
        explanation_parts.append(disease_context[disease])
    
    # Add confidence interpretation with actionable guidance
    confidence_pct = confidence * 100
    if confidence >= 0.75:
        explanation_parts.append(
            f"Confidence level: HIGH ({confidence_pct:.1f}%). "
            f"Strong diagnostic indicators detected. Recommend medical consultation for confirmation and treatment."
        )
    elif confidence >= 0.4:
        explanation_parts.append(
            f"Confidence level: MEDIUM ({confidence_pct:.1f}%). "
            f"Moderate diagnostic indicators. Clinical evaluation recommended for accurate diagnosis."
        )
    else:
        explanation_parts.append(
            f"Confidence level: LOW ({confidence_pct:.1f}%). "
            f"Uncertain diagnosis with weak indicators. Professional medical consultation strongly recommended."
        )
    
    # Add disclaimer
    explanation_parts.append(
        "⚠️ This is an AI-assisted preliminary assessment and should not replace "
        "professional medical diagnosis and treatment."
    )
    
    return " ".join(explanation_parts)
