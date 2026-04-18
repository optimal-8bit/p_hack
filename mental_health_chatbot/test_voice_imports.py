#!/usr/bin/env python3
"""
Test script to verify voice pipeline dependencies are installed correctly.
Run this before starting the server to catch any missing dependencies.
"""

import sys
import subprocess

def test_imports():
    """Test all required imports"""
    print("=" * 60)
    print("Testing Voice Pipeline Dependencies")
    print("=" * 60)
    
    errors = []
    
    # Test whisper
    print("\n1. Testing openai-whisper...")
    try:
        import whisper
        print("   ✓ openai-whisper imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import whisper: {e}")
        errors.append("openai-whisper")
    
    # Test librosa
    print("\n2. Testing librosa...")
    try:
        import librosa
        print("   ✓ librosa imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import librosa: {e}")
        errors.append("librosa")
    
    # Test soundfile
    print("\n3. Testing soundfile...")
    try:
        import soundfile
        print("   ✓ soundfile imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import soundfile: {e}")
        errors.append("soundfile")
    
    # Test ffmpeg-python
    print("\n4. Testing ffmpeg-python...")
    try:
        import ffmpeg
        print("   ✓ ffmpeg-python imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import ffmpeg-python: {e}")
        errors.append("ffmpeg-python")
    
    # Test ffmpeg binary
    print("\n5. Testing ffmpeg binary...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.decode().split('\n')[0]
            print(f"   ✓ ffmpeg binary found: {version_line}")
        else:
            print("   ✗ ffmpeg binary returned error")
            errors.append("ffmpeg binary")
    except FileNotFoundError:
        print("   ✗ ffmpeg binary not found in PATH")
        print("   Install from: https://ffmpeg.org/download.html")
        errors.append("ffmpeg binary")
    except Exception as e:
        print(f"   ✗ ffmpeg check failed: {e}")
        errors.append("ffmpeg binary")
    
    # Test voice module imports
    print("\n6. Testing voice module imports...")
    try:
        sys.path.insert(0, 'backend')
        from voice.transcriber import get_transcriber
        from voice.audio_analyzer import get_audio_analyzer
        from voice.word_attributor import get_word_attributor
        from voice.fusion_engine import get_fusion_engine
        from voice.voice_pipeline import get_voice_pipeline
        print("   ✓ All voice modules imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import voice modules: {e}")
        errors.append("voice modules")
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("❌ FAILED - Missing dependencies:")
        for error in errors:
            print(f"   - {error}")
        print("\nInstall missing dependencies:")
        print("   pip install -r backend/requirements.txt")
        if "ffmpeg binary" in errors:
            print("   Install ffmpeg from: https://ffmpeg.org/download.html")
        return False
    else:
        print("✅ SUCCESS - All dependencies installed correctly!")
        print("\nYou can now start the server:")
        print("   cd backend")
        print("   python main.py")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
