#!/usr/bin/env python3
"""
Script to download and convert models to ONNX format (classification only)
Translation models will use transformers directly (no ONNX export)
"""

import os
os.environ["PYTHONIOENCODING"] = "utf-8"

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

# Model configurations
CLASSIFICATION_MODELS = [
    {
        "name": "Emotion Classifier",
        "model_id": "j-hartmann/emotion-english-distilroberta-base",
        "output_dir": "../backend/onnx_models/emotion_classifier"
    },
    {
        "name": "Intent Classifier (NLI)",
        "model_id": "cross-encoder/nli-MiniLM2-L6-H768",
        "output_dir": "../backend/onnx_models/intent_classifier"
    },
]

TRANSLATION_MODELS = [
    {
        "name": "Hindi → English Translation",
        "model_id": "Helsinki-NLP/opus-mt-hi-en",
    },
    {
        "name": "English → Hindi Translation",
        "model_id": "Helsinki-NLP/opus-mt-en-hi",
    },
    {
        "name": "French → English Translation",
        "model_id": "Helsinki-NLP/opus-mt-fr-en",
    },
    {
        "name": "English → French Translation",
        "model_id": "Helsinki-NLP/opus-mt-en-fr",
    },
    {
        "name": "Spanish → English Translation",
        "model_id": "Helsinki-NLP/opus-mt-es-en",
    },
    {
        "name": "English → Spanish Translation",
        "model_id": "Helsinki-NLP/opus-mt-en-es",
    },
]


def download_classification_model(model_config):
    """Download and convert a classification model to ONNX with opset 18"""
    print(f"\n{'='*60}")
    print(f"Downloading: {model_config['name']}")
    print(f"Model ID: {model_config['model_id']}")
    print(f"Output: {model_config['output_dir']}")
    print(f"{'='*60}")
    
    try:
        from optimum.onnxruntime import ORTModelForSequenceClassification
        from transformers import AutoTokenizer
        
        # Create output directory
        output_path = Path(__file__).parent / model_config['output_dir']
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Loading model from HuggingFace...")
        
        # Load model and export to ONNX with opset 18 (no version conversion)
        model = ORTModelForSequenceClassification.from_pretrained(
            model_config['model_id'],
            export=True,
            provider="CPUExecutionProvider",
        )
        
        print(f"Saving ONNX model to {output_path}...")
        
        # Save model
        model.save_pretrained(str(output_path))
        
        # Also save tokenizer
        print(f"Saving tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_config['model_id'])
        tokenizer.save_pretrained(str(output_path))
        
        # Verify model.onnx exists
        model_file = output_path / "model.onnx"
        if model_file.exists():
            file_size = model_file.stat().st_size / (1024 * 1024)  # MB
            print(f"✓ Successfully exported {model_config['name']} ({file_size:.1f} MB)")
            return True
        else:
            print(f"✗ Export completed but model.onnx not found")
            return False
            
    except Exception as e:
        print(f"✗ Export failed for {model_config['name']}")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def download_translation_model(model_config):
    """Download translation model (transformers format, NOT ONNX)"""
    print(f"\n{'='*60}")
    print(f"Downloading: {model_config['name']}")
    print(f"Model ID: {model_config['model_id']}")
    print(f"Format: Transformers (NOT ONNX - will use at runtime)")
    print(f"{'='*60}")
    
    try:
        from transformers import MarianMTModel, MarianTokenizer
        
        print(f"Downloading model and tokenizer from HuggingFace...")
        
        # Just download the model to cache - will be loaded at runtime
        model = MarianMTModel.from_pretrained(model_config['model_id'])
        tokenizer = MarianTokenizer.from_pretrained(model_config['model_id'])
        
        print(f"✓ Successfully downloaded {model_config['name']} to cache")
        print(f"  (Will be loaded from cache at runtime)")
        return True
            
    except Exception as e:
        print(f"✗ Download failed for {model_config['name']}")
        print(f"Error: {str(e)}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Mental Health Chatbot - Model Download Script")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Export classification models to ONNX (emotion + intent)")
    print("2. Download translation models to cache (transformers format)")
    print("\nThis may take 10-20 minutes and requires ~1.5GB of disk space.")
    print()
    
    # Check if optimum is installed
    try:
        import optimum
        print("✓ optimum package is installed")
    except ImportError:
        print("✗ optimum package not found")
        print("Installing optimum[onnxruntime]...")
        import subprocess
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "optimum[onnxruntime]"],
                check=True
            )
            print("✓ optimum[onnxruntime] installed")
        except subprocess.CalledProcessError:
            print("✗ Failed to install optimum[onnxruntime]")
            print("Please run: pip install optimum[onnxruntime]")
            sys.exit(1)
    
    results = {}
    
    # Download classification models (ONNX export)
    print("\n" + "=" * 60)
    print("PHASE 1: Classification Models (ONNX Export)")
    print("=" * 60)
    
    for model_config in CLASSIFICATION_MODELS:
        success = download_classification_model(model_config)
        results[model_config['name']] = success
    
    # Download translation models (transformers format)
    print("\n" + "=" * 60)
    print("PHASE 2: Translation Models (Transformers Cache)")
    print("=" * 60)
    
    for model_config in TRANSLATION_MODELS:
        success = download_translation_model(model_config)
        results[model_config['name']] = success
    
    # Print summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    
    print("\nClassification Models (ONNX):")
    for model_config in CLASSIFICATION_MODELS:
        name = model_config['name']
        success = results.get(name, False)
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status}: {name}")
    
    print("\nTranslation Models (Transformers):")
    for model_config in TRANSLATION_MODELS:
        name = model_config['name']
        success = results.get(name, False)
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status}: {name}")
    
    # Count successes
    total = len(results)
    successful = sum(1 for s in results.values() if s)
    
    print(f"\nTotal: {successful}/{total} models successfully processed")
    
    # Check critical models (classification only)
    critical_models = ["Emotion Classifier", "Intent Classifier (NLI)"]
    critical_success = all(results.get(m, False) for m in critical_models)
    
    if critical_success:
        print("\n✓ All critical models (emotion + intent) are ready!")
        print("  → ONNX models exported successfully")
        print("  → Translation will use transformers at runtime")
        print("\nThe server can now run with full functionality.")
    else:
        print("\n⚠ Some critical models failed to export.")
        print("  → The server will use rule-based fallbacks for missing models.")
        print("  → This is acceptable for demo purposes.")
    
    print("\nNext steps:")
    print("1. Run: python scripts/verify_models.py")
    print("2. Run: cd backend && python main.py")
    print("=" * 60)
    
    return 0 if critical_success else 1


if __name__ == "__main__":
    sys.exit(main())
