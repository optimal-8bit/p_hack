#!/usr/bin/env python3
"""
Script to download and convert all models to ONNX format
Run this before starting the server for the first time
"""

import subprocess
import sys
from pathlib import Path

# Model configurations
MODELS = [
    {
        "name": "Emotion Classifier",
        "model_id": "j-hartmann/emotion-english-distilroberta-base",
        "task": "text-classification",
        "output_dir": "../backend/onnx_models/emotion_classifier"
    },
    {
        "name": "Intent Classifier (NLI)",
        "model_id": "cross-encoder/nli-MiniLM2-L6-H768",
        "task": "text-classification",
        "output_dir": "../backend/onnx_models/intent_classifier"
    },
    {
        "name": "Hindi → English Translation",
        "model_id": "Helsinki-NLP/opus-mt-hi-en",
        "task": "seq2seq-lm",
        "output_dir": "../backend/onnx_models/translate_hi_en"
    },
    {
        "name": "English → Hindi Translation",
        "model_id": "Helsinki-NLP/opus-mt-en-hi",
        "task": "seq2seq-lm",
        "output_dir": "../backend/onnx_models/translate_en_hi"
    },
    {
        "name": "French → English Translation",
        "model_id": "Helsinki-NLP/opus-mt-fr-en",
        "task": "seq2seq-lm",
        "output_dir": "../backend/onnx_models/translate_fr_en"
    },
    {
        "name": "English → French Translation",
        "model_id": "Helsinki-NLP/opus-mt-en-fr",
        "task": "seq2seq-lm",
        "output_dir": "../backend/onnx_models/translate_en_fr"
    },
    {
        "name": "Spanish → English Translation",
        "model_id": "Helsinki-NLP/opus-mt-es-en",
        "task": "seq2seq-lm",
        "output_dir": "../backend/onnx_models/translate_es_en"
    },
    {
        "name": "English → Spanish Translation",
        "model_id": "Helsinki-NLP/opus-mt-en-es",
        "task": "seq2seq-lm",
        "output_dir": "../backend/onnx_models/translate_en_es"
    },
]


def check_optimum_cli():
    """Check if optimum-cli is installed"""
    try:
        result = subprocess.run(
            ["optimum-cli", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ optimum-cli is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ optimum-cli not found")
    print("Installing optimum[exporters]...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "optimum[exporters]"],
            check=True
        )
        print("✓ optimum[exporters] installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install optimum[exporters]")
        return False


def download_model(model_config):
    """Download and convert a single model to ONNX"""
    print(f"\n{'='*60}")
    print(f"Downloading: {model_config['name']}")
    print(f"Model ID: {model_config['model_id']}")
    print(f"Output: {model_config['output_dir']}")
    print(f"{'='*60}")
    
    # Create output directory
    output_path = Path(__file__).parent / model_config['output_dir']
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Build command
    cmd = [
        "optimum-cli",
        "export",
        "onnx",
        "--model", model_config['model_id'],
        "--task", model_config['task'],
        str(output_path)
    ]
    
    try:
        # Run export
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            # Verify model.onnx exists
            model_file = output_path / "model.onnx"
            if model_file.exists():
                print(f"✓ Successfully exported {model_config['name']}")
                return True
            else:
                print(f"✗ Export completed but model.onnx not found")
                return False
        else:
            print(f"✗ Export failed for {model_config['name']}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ Export timed out for {model_config['name']}")
        return False
    except Exception as e:
        print(f"✗ Error exporting {model_config['name']}: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Mental Health Chatbot - Model Download Script")
    print("=" * 60)
    print("\nThis script will download and convert all required models to ONNX format.")
    print("This may take 15-30 minutes and requires ~2GB of disk space.")
    print("\nNote: Translation model exports may fail (known issue with seq2seq models).")
    print("The system will automatically fall back to using transformers directly.")
    print()
    
    # Check optimum-cli
    if not check_optimum_cli():
        print("\n✗ Cannot proceed without optimum-cli")
        sys.exit(1)
    
    # Download all models
    results = {}
    for model_config in MODELS:
        success = download_model(model_config)
        results[model_config['name']] = success
    
    # Print summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    
    for name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {name}")
    
    # Count successes
    total = len(results)
    successful = sum(1 for s in results.values() if s)
    
    print(f"\nTotal: {successful}/{total} models successfully exported")
    
    # Check critical models
    critical_models = ["Emotion Classifier", "Intent Classifier (NLI)"]
    critical_success = all(results.get(m, False) for m in critical_models)
    
    if critical_success:
        print("\n✓ All critical models (emotion + intent) are ready!")
        print("The server can now run with full ONNX inference.")
    else:
        print("\n⚠ Some critical models failed to export.")
        print("The server will use rule-based fallbacks for missing models.")
    
    print("\nNext steps:")
    print("1. Run: python scripts/verify_models.py")
    print("2. Run: cd backend && python main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
