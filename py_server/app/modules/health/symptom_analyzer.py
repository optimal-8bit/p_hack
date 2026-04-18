"""
Symptom-based disease analysis using rule-based system.
"""
from typing import Dict, List

# Symptom-to-disease mapping with weights
SYMPTOM_RULES: Dict[str, Dict[str, float]] = {
    "itching": {
        "fungal infection": 0.3,
        "eczema": 0.25,
        "psoriasis": 0.15,
        "bacterial infection": 0.1
    },
    "redness": {
        "eczema": 0.2,
        "psoriasis": 0.15,
        "bacterial infection": 0.2,
        "fungal infection": 0.15
    },
    "fever": {
        "bacterial infection": 0.3,
        "fungal infection": 0.1,
        "eczema": 0.05,
        "psoriasis": 0.05
    },
    "cough": {
        "bacterial infection": 0.2,
        "fungal infection": 0.05,
        "eczema": 0.0,
        "psoriasis": 0.0
    },
    "fatigue": {
        "psoriasis": 0.1,
        "bacterial infection": 0.15,
        "fungal infection": 0.1,
        "eczema": 0.08
    }
}

# All possible diseases
DISEASES = [
    "fungal infection",
    "eczema",
    "psoriasis",
    "bacterial infection"
]


def analyze_symptoms(symptoms: List[str]) -> Dict[str, float]:
    """
    Analyze symptoms and return disease probabilities.
    
    Args:
        symptoms: List of symptom names
        
    Returns:
        Dictionary mapping disease names to probabilities
    """
    # Initialize scores for all diseases
    disease_scores: Dict[str, float] = {disease: 0.0 for disease in DISEASES}
    
    # If no symptoms provided, return uniform distribution
    if not symptoms:
        uniform_score = 1.0 / len(DISEASES)
        return {disease: uniform_score for disease in DISEASES}
    
    # Accumulate scores from each symptom
    for symptom in symptoms:
        symptom_lower = symptom.lower().strip()
        
        if symptom_lower in SYMPTOM_RULES:
            for disease, weight in SYMPTOM_RULES[symptom_lower].items():
                disease_scores[disease] += weight
    
    # Normalize scores to sum to 1.0
    total_score = sum(disease_scores.values())
    
    if total_score > 0:
        normalized_scores = {
            disease: score / total_score
            for disease, score in disease_scores.items()
        }
    else:
        # If no matching symptoms, return uniform distribution
        uniform_score = 1.0 / len(DISEASES)
        normalized_scores = {disease: uniform_score for disease in DISEASES}
    
    return normalized_scores


def get_valid_symptoms() -> List[str]:
    """
    Get list of valid symptom names.
    
    Returns:
        List of valid symptom names
    """
    return list(SYMPTOM_RULES.keys())
