# Installation Fix for Voice Pipeline

## Issue
The `openai-whisper==20231117` package has build issues. We need to install dependencies in the correct order.

## Solution

Run these commands in order:

```bash
# 1. Upgrade pip and install build tools
python -m pip install --upgrade pip setuptools wheel

# 2. Install openai-whisper (use latest stable version)
pip install openai-whisper

# 3. Install other dependencies
pip install librosa==0.10.1
pip install soundfile==0.12.1
pip install ffmpeg-python==0.2.0

# 4. Verify installation
cd ..
python test_voice_imports.py
```

## Alternative: Install All at Once

```bash
# Upgrade tools first
python -m pip install --upgrade pip setuptools wheel

# Then install all voice dependencies
pip install openai-whisper librosa==0.10.1 soundfile==0.12.1 ffmpeg-python==0.2.0
```

## If Still Having Issues

Try installing without version pinning:

```bash
pip install openai-whisper librosa soundfile ffmpeg-python
```

The code is compatible with any recent version of these packages.
