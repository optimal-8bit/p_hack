"""
Test script for ONNX-based health diagnostic pipeline.
Tests the complete flow: image → ONNX model → pattern mapping → decision engine → disease
"""
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def test_model_loading():
    """Test 1: Verify ONNX model loads correctly"""
    logger.info("=" * 60)
    logger.info("TEST 1: Model Loading")
    logger.info("=" * 60)
    
    from app.modules.health.ai_engine import _load_onnx_model, MODEL_PATH
    
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Model exists: {MODEL_PATH.exists()}")
    
    if MODEL_PATH.exists():
        logger.info(f"Model size: {MODEL_PATH.stat().st_size / (1024*1024):.2f} MB")
    
    success = _load_onnx_model()
    
    if success:
        logger.info("✓ Model loaded successfully")
        return True
    else:
        logger.warning("✗ Model loading failed (will use fallback)")
        return False


def test_image_preprocessing():
    """Test 2: Verify image preprocessing works"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Image Preprocessing")
    logger.info("=" * 60)
    
    from app.modules.health.ai_engine import _preprocess_image
    from PIL import Image
    import numpy as np
    import io
    
    # Create a test image (224x224 RGB)
    test_image = Image.new('RGB', (300, 300), color='red')
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    test_image.save(img_byte_arr, format='PNG')
    image_bytes = img_byte_arr.getvalue()
    
    logger.info(f"Test image size: {len(image_bytes)} bytes")
    
    # Preprocess
    result = _preprocess_image(image_bytes)
    
    if result is not None:
        logger.info(f"✓ Preprocessing successful")
        logger.info(f"  Output shape: {result.shape}")
        logger.info(f"  Output dtype: {result.dtype}")
        logger.info(f"  Value range: [{result.min():.3f}, {result.max():.3f}]")
        
        # Verify shape
        assert result.shape == (1, 3, 224, 224), f"Expected (1, 3, 224, 224), got {result.shape}"
        logger.info("✓ Shape is correct (1, 3, 224, 224)")
        
        # Verify normalization
        assert 0 <= result.min() <= 1, "Values should be normalized to [0, 1]"
        assert 0 <= result.max() <= 1, "Values should be normalized to [0, 1]"
        logger.info("✓ Normalization is correct [0, 1]")
        
        return True
    else:
        logger.error("✗ Preprocessing failed")
        return False


def test_onnx_inference():
    """Test 3: Verify ONNX inference runs"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: ONNX Inference")
    logger.info("=" * 60)
    
    from app.modules.health.ai_engine import analyze_image
    from PIL import Image
    import io
    
    # Create test images with different colors
    test_cases = [
        ("Red image", (255, 0, 0)),
        ("Green image", (0, 255, 0)),
        ("Blue image", (0, 0, 255)),
    ]
    
    for name, color in test_cases:
        logger.info(f"\nTesting: {name}")
        
        # Create test image
        test_image = Image.new('RGB', (224, 224), color=color)
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='PNG')
        image_bytes = img_byte_arr.getvalue()
        
        # Run inference
        result = analyze_image(image_bytes)
        
        logger.info(f"  Results: {result}")
        
        # Verify result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert len(result) > 0, "Result should not be empty"
        
        # Verify probabilities sum to ~1.0
        total = sum(result.values())
        logger.info(f"  Total probability: {total:.3f}")
        assert 0.95 <= total <= 1.05, f"Probabilities should sum to ~1.0, got {total}"
        
        # Show top prediction
        top_disease = max(result.items(), key=lambda x: x[1])
        logger.info(f"  ✓ Top prediction: {top_disease[0]} ({top_disease[1]:.3f})")
    
    return True


def test_symptom_analysis():
    """Test 4: Verify symptom analysis"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: Symptom Analysis")
    logger.info("=" * 60)
    
    from app.modules.health.symptom_analyzer import analyze_symptoms
    
    test_cases = [
        (["itching", "redness"], "Itching + Redness"),
        (["fever", "cough"], "Fever + Cough"),
        (["fatigue"], "Fatigue only"),
        ([], "No symptoms"),
    ]
    
    for symptoms, description in test_cases:
        logger.info(f"\nTesting: {description}")
        logger.info(f"  Symptoms: {symptoms}")
        
        result = analyze_symptoms(symptoms)
        
        logger.info(f"  Results: {result}")
        
        # Verify result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify probabilities sum to ~1.0
        total = sum(result.values())
        logger.info(f"  Total probability: {total:.3f}")
        assert 0.95 <= total <= 1.05, f"Probabilities should sum to ~1.0, got {total}"
        
        # Show top prediction
        top_disease = max(result.items(), key=lambda x: x[1])
        logger.info(f"  ✓ Top prediction: {top_disease[0]} ({top_disease[1]:.3f})")
    
    return True


def test_decision_engine():
    """Test 5: Verify decision engine combines scores correctly"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 5: Decision Engine")
    logger.info("=" * 60)
    
    from app.modules.health.decision_engine import (
        combine_scores,
        get_top_prediction,
        calculate_risk_level,
        generate_explanation
    )
    
    # Test score combination
    image_scores = {
        "fungal infection": 0.6,
        "eczema": 0.2,
        "psoriasis": 0.15,
        "bacterial infection": 0.05
    }
    
    symptom_scores = {
        "fungal infection": 0.3,
        "eczema": 0.4,
        "psoriasis": 0.2,
        "bacterial infection": 0.1
    }
    
    logger.info(f"Image scores: {image_scores}")
    logger.info(f"Symptom scores: {symptom_scores}")
    
    # Combine (70% image, 30% symptom)
    combined = combine_scores(image_scores, symptom_scores)
    logger.info(f"Combined scores: {combined}")
    
    # Verify total
    total = sum(combined.values())
    logger.info(f"Total probability: {total:.3f}")
    assert 0.95 <= total <= 1.05, f"Combined probabilities should sum to ~1.0, got {total}"
    
    # Get top prediction
    disease, confidence = get_top_prediction(combined)
    logger.info(f"✓ Top prediction: {disease} (confidence: {confidence:.3f})")
    
    # Calculate risk level
    risk = calculate_risk_level(confidence)
    logger.info(f"✓ Risk level: {risk}")
    
    # Generate explanation
    explanation = generate_explanation(disease, confidence, ["itching", "redness"], True)
    logger.info(f"✓ Explanation generated ({len(explanation)} chars)")
    logger.info(f"  Preview: {explanation[:150]}...")
    
    return True


def test_complete_pipeline():
    """Test 6: End-to-end pipeline test"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 6: Complete Pipeline")
    logger.info("=" * 60)
    
    from app.modules.health.ai_engine import analyze_image
    from app.modules.health.symptom_analyzer import analyze_symptoms
    from app.modules.health.decision_engine import (
        combine_scores,
        get_top_prediction,
        calculate_risk_level,
        generate_explanation
    )
    from PIL import Image
    import io
    
    # Create test image
    test_image = Image.new('RGB', (224, 224), color=(200, 100, 100))
    img_byte_arr = io.BytesIO()
    test_image.save(img_byte_arr, format='PNG')
    image_bytes = img_byte_arr.getvalue()
    
    # Test symptoms
    symptoms = ["itching", "redness"]
    
    logger.info(f"Input: {symptoms} + image")
    
    # Step 1: Analyze image
    logger.info("\nStep 1: Analyzing image...")
    image_scores = analyze_image(image_bytes)
    logger.info(f"  Image scores: {image_scores}")
    
    # Step 2: Analyze symptoms
    logger.info("\nStep 2: Analyzing symptoms...")
    symptom_scores = analyze_symptoms(symptoms)
    logger.info(f"  Symptom scores: {symptom_scores}")
    
    # Step 3: Combine scores
    logger.info("\nStep 3: Combining scores...")
    combined_scores = combine_scores(image_scores, symptom_scores)
    logger.info(f"  Combined scores: {combined_scores}")
    
    # Step 4: Get prediction
    logger.info("\nStep 4: Getting top prediction...")
    disease, confidence = get_top_prediction(combined_scores)
    logger.info(f"  Disease: {disease}")
    logger.info(f"  Confidence: {confidence:.3f}")
    
    # Step 5: Calculate risk
    logger.info("\nStep 5: Calculating risk level...")
    risk_level = calculate_risk_level(confidence)
    logger.info(f"  Risk level: {risk_level}")
    
    # Step 6: Generate explanation
    logger.info("\nStep 6: Generating explanation...")
    explanation = generate_explanation(disease, confidence, symptoms, True)
    logger.info(f"  Explanation: {explanation}")
    
    # Final result
    logger.info("\n" + "=" * 60)
    logger.info("FINAL DIAGNOSIS RESULT")
    logger.info("=" * 60)
    logger.info(f"Disease: {disease}")
    logger.info(f"Confidence: {confidence:.1%}")
    logger.info(f"Risk Level: {risk_level}")
    logger.info(f"Explanation: {explanation}")
    logger.info("=" * 60)
    
    return True


def main():
    """Run all tests"""
    logger.info("\n" + "=" * 60)
    logger.info("ONNX HEALTH DIAGNOSTIC PIPELINE TEST SUITE")
    logger.info("=" * 60)
    
    tests = [
        ("Model Loading", test_model_loading),
        ("Image Preprocessing", test_image_preprocessing),
        ("ONNX Inference", test_onnx_inference),
        ("Symptom Analysis", test_symptom_analysis),
        ("Decision Engine", test_decision_engine),
        ("Complete Pipeline", test_complete_pipeline),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"✗ {test_name} failed with error: {e}", exc_info=True)
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("=" * 60)
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
