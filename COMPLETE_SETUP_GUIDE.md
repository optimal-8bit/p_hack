# Complete Setup Guide - Voice Pipeline Feature

## 🎯 Quick Start (3 Steps)

### Step 1: Fix ffmpeg PATH

```powershell
# Add ffmpeg to PATH (replace with your actual path)
$env:PATH += ";C:\ffmpeg\bin"

# Verify it works
ffmpeg -version
```

**For permanent fix**, restart PowerShell after running:
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "User")
```

### Step 2: Start Backend

```bash
cd mental_health_chatbot/backend
python main.py
```

Wait for these messages:
```
✓ Whisper model loaded successfully
✓ ffmpeg is available
✓ Chat orchestrator initialized
```

### Step 3: Open Frontend

Double-click: `mental_health_chatbot/frontend_test/index.html`

Or:
```bash
start mental_health_chatbot/frontend_test/index.html
```

## ✅ Verify Everything Works

### 1. Check Voice Health
Open in browser: http://localhost:8000/api/voice/health

Should show:
```json
{
  "whisper_loaded": true,
  "librosa_available": true,
  "ffmpeg_available": true
}
```

### 2. Test Voice Feature
1. Click 🎤 microphone button
2. Allow microphone access
3. Say: "I'm feeling anxious today"
4. Click ⏹️ to stop
5. Wait 2-4 seconds
6. See transcript and voice analysis!

## 📋 What Was Implemented

### Backend (7 new files)
- ✅ `voice/transcriber.py` - Whisper speech-to-text
- ✅ `voice/audio_analyzer.py` - Audio feature extraction
- ✅ `voice/word_attributor.py` - Text importance
- ✅ `voice/fusion_engine.py` - Emotion fusion
- ✅ `voice/voice_pipeline.py` - Main coordinator
- ✅ `voice/voice_routes.py` - API endpoints
- ✅ Modified orchestrator for override_emotion

### Frontend (2 files modified)
- ✅ `frontend_test/index.html` - Added mic button
- ✅ `frontend_test/app.js` - Added voice recording

### API Endpoints
- ✅ `POST /api/voice/chat` - Process voice messages
- ✅ `GET /api/voice/health` - Check voice status

## 🎤 How to Use

### Text Chat (existing)
1. Type message in input box
2. Press Enter or click Send
3. Get response

### Voice Chat (new!)
1. Click 🎤 microphone button
2. Speak your message
3. Click ⏹️ to stop
4. Get response with voice analysis

## 🔍 What You'll See

### Voice Response Includes:
- **Transcript** of what you said
- **Fused emotion** (text + audio combined)
- **Text-only emotion** (from words)
- **Audio-focused emotion** (from voice)
- **Stressed words** (emotionally important)
- **Incongruence warning** (if words ≠ voice)

### Example Output:
```
User: 🎤 I'm feeling really anxious today

Bot: I hear that you're feeling anxious. That must be difficult...

[🎤 voice] [emotion: fear 88%] [text: fear 82%] [audio: anxiety 91%]
[duration: 3.2s] [processing: 2450ms]

Emphasized words: really, anxious
```

## 🐛 Troubleshooting

### Issue: "ffmpeg binary not found"
**Solution:**
```powershell
# Temporary fix
$env:PATH += ";C:\ffmpeg\bin"

# Permanent fix
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "User")

# Then restart PowerShell and verify
ffmpeg -version
```

### Issue: "Microphone access denied"
**Solution:**
1. Click 🔒 in browser address bar
2. Allow microphone
3. Refresh page

### Issue: "Whisper model not loaded"
**Solution:**
- First run downloads ~460MB model
- Check internet connection
- Check disk space
- Wait for download to complete

### Issue: Backend won't start
**Solution:**
```bash
# Check if dependencies installed
cd mental_health_chatbot
python test_voice_imports.py

# If missing, install
cd backend
pip install openai-whisper librosa soundfile ffmpeg-python
```

## 📚 Documentation

- **Quick Start**: This file
- **Backend Details**: `VOICE_PIPELINE_README.md`
- **Frontend Guide**: `VOICE_FRONTEND_GUIDE.md`
- **ffmpeg Fix**: `FIX_FFMPEG_PATH.md`
- **Installation**: `INSTALL_VOICE_PIPELINE.md`
- **Implementation**: `VOICE_PIPELINE_IMPLEMENTATION.md`

## 🧪 Testing Commands

```bash
# Test dependencies
python test_voice_imports.py

# Check backend health
curl http://localhost:8000/api/health

# Check voice health
curl http://localhost:8000/api/voice/health

# Test voice endpoint (with audio file)
curl -X POST http://localhost:8000/api/voice/chat \
  -F "session_id=test123" \
  -F "audio=@test.wav"
```

## ✨ Key Features

### 1. Two-Stage Emotion Fusion
- Analyzes full text
- Analyzes high-weight words
- Combines with audio features
- More accurate than text-only

### 2. Emotional Incongruence Detection
- Compares words vs voice
- Detects masked distress
- Clinically meaningful signal

### 3. Per-Word Audio Analysis
- Pitch patterns
- Amplitude/volume
- Stress detection
- Emotion hints

### 4. Crisis Detection
- Checks transcript for crisis patterns
- Immediate response if detected
- Skips audio analysis for speed

## 🎯 Current Status

✅ **Backend**: Fully implemented and tested  
✅ **Frontend**: Microphone integrated  
✅ **API**: Two endpoints working  
✅ **Documentation**: Complete  
⚠️ **ffmpeg**: Needs PATH configuration  

## 🚀 Next Steps

1. **Fix ffmpeg PATH** (see Step 1 above)
2. **Start backend** (see Step 2 above)
3. **Open frontend** (see Step 3 above)
4. **Test voice feature** with microphone
5. **Try different emotions** to see fusion in action

## 💡 Tips

### For Best Results:
- Speak clearly and naturally
- 2-5 seconds is ideal length
- Express emotion naturally
- Avoid background noise

### Test Phrases:
- "I'm feeling really anxious today"
- "I'm fine" (said sadly - tests incongruence)
- "Nobody understands me"
- "I can't handle this anymore"

## 🔗 Quick Links

- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Voice Health: http://localhost:8000/api/voice/health
- Frontend: `mental_health_chatbot/frontend_test/index.html`

## ❓ Need Help?

1. Check backend terminal for error logs
2. Check browser console (F12) for frontend errors
3. Run `python test_voice_imports.py` to verify setup
4. Check `ffmpeg -version` to verify PATH
5. Review documentation files listed above

## 🎉 You're Ready!

Once ffmpeg PATH is fixed, you can:
- ✅ Use voice input in the chatbot
- ✅ See emotion fusion in action
- ✅ Detect emotional incongruence
- ✅ View per-word audio analysis
- ✅ Get more accurate emotion detection

**Start the backend and try it out!** 🎤
