#!/usr/bin/env python3
"""
Quick installation check script
Verifies all dependencies are installed correctly
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (need 3.11+)")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "onnxruntime",
        "transformers",
        "langdetect",
        "sqlalchemy",
        "aiosqlite",
        "numpy",
        "pytest"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_directory_structure():
    """Check if directory structure is correct"""
    print("\nChecking directory structure...")
    
    base_dir = Path(__file__).parent.parent
    
    required_dirs = [
        "backend",
        "backend/models",
        "backend/pipeline",
        "backend/response_engine",
        "backend/api",
        "backend/database",
        "backend/onnx_models",
        "backend/tests",
        "frontend_test",
        "scripts"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/")
            all_exist = False
    
    return all_exist


def check_config_files():
    """Check if configuration files exist"""
    print("\nChecking configuration files...")
    
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "backend/config.py",
        "backend/main.py",
        "backend/requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            all_exist = False
    
    return all_exist


def check_models():
    """Check if ONNX models are downloaded"""
    print("\nChecking ONNX models...")
    
    base_dir = Path(__file__).parent.parent
    models_dir = base_dir / "backend" / "onnx_models"
    
    model_dirs = [
        "emotion_classifier",
        "intent_classifier",
        "translate_hi_en",
        "translate_en_hi"
    ]
    
    found_models = []
    for model_dir in model_dirs:
        model_path = models_dir / model_dir / "model.onnx"
        if model_path.exists():
            print(f"✓ {model_dir}")
            found_models.append(model_dir)
        else:
            print(f"⚠ {model_dir} (not downloaded)")
    
    if len(found_models) >= 2:
        print("\n✓ Critical models (emotion + intent) are available")
        return True
    else:
        print("\n⚠ Models not downloaded. Run: python scripts/download_models.py")
        print("  (System will work with rule-based fallbacks)")
        return False


def main():
    """Main check function"""
    print("=" * 60)
    print("Mental Health Chatbot - Installation Check")
    print("=" * 60)
    
    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies()[0],
        "Directory Structure": check_directory_structure(),
        "Config Files": check_config_files(),
        "ONNX Models": check_models()
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to run the backend.")
        print("\nNext steps:")
        print("  1. cd backend")
        print("  2. python main.py")
        print("  3. Open frontend_test/index.html in browser")
    else:
        print("\n⚠ Some checks failed. Please fix the issues above.")
        
        if not results["Dependencies"]:
            print("\nTo install dependencies:")
            print("  pip install -r backend/requirements.txt")
        
        if not results["ONNX Models"]:
            print("\nTo download models (optional but recommended):")
            print("  python scripts/download_models.py")
    
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
