# How to Test Voice Feature (Step by Step)

## ⚠️ IMPORTANT: Two Different Endpoints

Your chatbot has **TWO** ways to send messages:

### 1. Text Chat (What you just used)
- Type in the text box → Press Enter or click "Send"
- Endpoint: `POST /api/chat`
- **NO audio analysis** - just text processing
- Logs show: `Processing message for session...`

### 2. Voice Chat (What you need to test)
- Click 🎤 microphone button → Speak → Click ⏹️ stop
- Endpoint: `POST /api/voice/chat`
- **FULL audio analysis** - pitch, amplitude, fusion, etc.
- Logs show: `Transcribing audio...`, `Analyzing audio features...`, etc.

## 🎯 How to Test Voice Feature

### Step 1: Make Sure Backend is Running
You already have it running! ✅

### Step 2: Open Frontend
Double-click: `mental_health_chatbot/frontend_test/index.html`

### Step 3: Use the MICROPHONE Button
**DO NOT type in the text box!**

1. Click the **🎤 button** (next to the Send button)
2. Browser will ask for microphone permission → Click "Allow"
3. You'll see "Recording... Click stop when done"
4. **Speak clearly**: "I'm feeling really anxious today"
5. Click the **⏹️ button** to stop
6. Wait 2-4 seconds

### Step 4: Watch Backend Terminal
You should see:

```
INFO - Transcribing audio for session...
INFO - Transcription complete in 1200ms: I'm feeling really anxious today
INFO - Analyzing audio features
INFO - 📊 Speaker baseline: pitch=180.5Hz, amplitude=0.045
INFO - ✓ Analyzed 6 words from audio
INFO - ✓ Computed text weights for 6 words
INFO - Running fusion engine
INFO - 🎯 Text-only emotion: fear (0.82)
INFO - 🎵 Audio-focused emotion: fear (0.91)
INFO - ⚡ FUSED emotion: fear (0.88)
INFO - 💪 Stressed words: really, anxious
INFO - Calling orchestrator for response generation
```

### Step 5: Check Frontend Response
You should see:

```
User: 🎤 I'm feeling really anxious today

Bot: [Response text]

[🎤 voice] [emotion: fear 88%] [text: fear 82%] [audio: anxiety 91%]
[duration: 3.2s] [processing: 2450ms]

Emphasized words: really, anxious
```

## 🔍 What You Tested Before

Looking at your logs:
```
INFO: 127.0.0.1:52190 - "POST /api/chat HTTP/1.1" 200 OK
```

This is the **TEXT endpoint** - no audio processing happens here!

You need to see:
```
INFO: 127.0.0.1:xxxxx - "POST /api/voice/chat HTTP/1.1" 200 OK
```

## 🎤 Quick Visual Test

### Text Chat (No Audio Analysis)
```
┌─────────────────────────────┐
│ Type message here...        │
└─────────────────────────────┘
                    [🎤] [Send]
                     ↑
              DON'T USE THIS
              FOR TEXT CHAT
```

### Voice Chat (Full Audio Analysis)
```
┌─────────────────────────────┐
│ Type message here...        │
└─────────────────────────────┘
                    [🎤] [Send]
                     ↑
              CLICK THIS!
              THEN SPEAK
```

## 🧪 Test Script (If Frontend Doesn't Work)

If the frontend microphone isn't working, test directly with curl:

```bash
# Record a test audio file first (use any audio recorder)
# Then test:

curl -X POST http://localhost:8000/api/voice/chat \
  -F "session_id=test123" \
  -F "audio=@test_audio.wav"
```

## 🐛 Troubleshooting

### "I clicked 🎤 but nothing happened"
- Check browser console (F12) for errors
- Make sure you allowed microphone permissions
- Try refreshing the page

### "Recording works but no response"
- Check backend terminal for errors
- Look for `POST /api/voice/chat` in logs
- Check if ffmpeg is in PATH: `ffmpeg -version`

### "I only see text processing logs"
- You're using the text input, not the microphone!
- Click 🎤, don't type in the box

## ✅ Success Indicators

You'll know it's working when you see:

**Backend logs:**
- ✅ `Transcribing audio for session...`
- ✅ `📊 Speaker baseline: pitch=...`
- ✅ `✓ Analyzed X words from audio`
- ✅ `🎯 Text-only emotion: ...`
- ✅ `🎵 Audio-focused emotion: ...`
- ✅ `⚡ FUSED emotion: ...`

**Frontend:**
- ✅ User message shows 🎤 icon
- ✅ Response shows `[🎤 voice]` metadata
- ✅ Shows text vs audio emotion comparison
- ✅ Shows emphasized words

## 📝 Summary

**What you tested:** Text chat (typing) → No audio analysis ❌
**What you need:** Voice chat (microphone) → Full audio analysis ✅

**Try again with the 🎤 button and watch the backend logs!**
