# Quick Installation Guide - Voice Pipeline

## Step 1: Activate Your Virtual Environment

```bash
# Use whatever command you normally use to activate your venv
# For example:
# source venv/bin/activate  (Linux/Mac)
# venv\Scripts\activate     (Windows)
```

## Step 2: Install Python Dependencies

```bash
cd mental_health_chatbot/backend
pip install openai-whisper==20231117
pip install librosa==0.10.1
pip install soundfile==0.12.1
pip install ffmpeg-python==0.2.0
```

Or install all at once:
```bash
pip install openai-whisper==20231117 librosa==0.10.1 soundfile==0.12.1 ffmpeg-python==0.2.0
```

## Step 3: Install ffmpeg (System-Level)

### Windows (Chocolatey)
```bash
choco install ffmpeg
```

### Windows (Manual)
1. Download from: https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to your PATH environment variable

### Linux
```bash
sudo apt-get install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

## Step 4: Verify Installation

```bash
cd mental_health_chatbot
python test_voice_imports.py
```

You should see:
```
✅ SUCCESS - All dependencies installed correctly!
```

## Step 5: Start the Server

```bash
cd backend
python main.py
```

Watch for these log messages:
```
✓ Whisper model loaded successfully
✓ ffmpeg is available
```

**Note:** On first run, Whisper will download a ~460MB model. This is normal and only happens once.

## Step 6: Test the Voice Endpoint

### Check Health
```bash
curl http://localhost:8000/api/voice/health
```

Expected response:
```json
{
  "whisper_loaded": true,
  "whisper_model": "small",
  "librosa_available": true,
  "ffmpeg_available": true,
  "supported_formats": [".wav", ".mp3", ".m4a", ".webm", ".ogg"],
  "max_file_size_mb": 10
}
```

### Test with Audio File
```bash
curl -X POST http://localhost:8000/api/voice/chat \
  -F "session_id=test123" \
  -F "audio=@your_audio_file.wav"
```

## Troubleshooting

### "Module not found" errors
- Make sure you're in the correct virtual environment
- Re-run: `pip install openai-whisper librosa soundfile ffmpeg-python`

### "ffmpeg not found"
- Install ffmpeg system-wide (not via pip)
- Verify with: `ffmpeg -version`
- On Windows, make sure ffmpeg is in your PATH

### "Whisper model download failed"
- Check internet connection
- Check disk space (~500MB needed)
- Try running again (download may have been interrupted)

### Server won't start
- Check if port 8000 is already in use
- Look at the error message in the terminal
- Make sure you're in the `backend` directory

## What's Next?

Once installed, you can:
1. Use the voice chat endpoint: `POST /api/voice/chat`
2. Check the full documentation: `mental_health_chatbot/VOICE_PIPELINE_README.md`
3. Test with different audio formats (.wav, .mp3, .m4a, .webm, .ogg)
4. Integrate with your frontend

## Quick Test

Create a simple test:
```python
import requests

# Test voice chat
with open("test_audio.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/voice/chat",
        data={"session_id": "test123"},
        files={"audio": f}
    )
    print(response.json())
```

## Need Help?

- Check `VOICE_PIPELINE_README.md` for detailed documentation
- Run `python test_voice_imports.py` to diagnose issues
- Check server logs for error messages
- Visit `/docs` endpoint for interactive API documentation
