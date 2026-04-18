# Visual Guide - Text vs Voice Chat

## What You See in the Frontend

```
┌─────────────────────────────────────────────────────────┐
│  Mental Health Chatbot                                  │
│  Session ID: abc-123                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Chat messages appear here]                            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────┐                 │
│  │ Type your message here...         │                 │
│  └───────────────────────────────────┘                 │
│                                                         │
│                          [🎤]    [Send]                 │
│                         Voice     Text                  │
│                           ↑        ↑                    │
│                           │        │                    │
│                    AUDIO ANALYSIS  │                    │
│                    (What you want) │                    │
│                                    │                    │
│                              TEXT ONLY                  │
│                           (No audio analysis)           │
└─────────────────────────────────────────────────────────┘
```

## Two Different Workflows

### ❌ Text Chat (What you tested)
```
1. Type: "I'm feeling anxious"
2. Press Enter or click [Send]
3. Backend receives: TEXT ONLY
4. Processing: Text → Emotion → Response
5. NO audio analysis
6. Logs: "Processing message for session..."
```

### ✅ Voice Chat (What you need to test)
```
1. Click [🎤] button
2. Speak: "I'm feeling anxious"
3. Click [⏹️] to stop
4. Backend receives: AUDIO FILE
5. Processing: 
   - Transcribe audio → text
   - Analyze audio → pitch, amplitude, stress
   - Compute text weights
   - FUSE audio + text → better emotion
6. Logs: "Transcribing audio...", "Analyzing audio features...", etc.
```

## Backend Logs Comparison

### Text Chat Logs (No Audio)
```
INFO - Processing message for session session-123
INFO - Message type: neutral (confidence: 0.70)
INFO - Detected language: en (confidence: 1.00)
INFO - Processed message in 11630ms
INFO: POST /api/chat HTTP/1.1 200 OK
```

### Voice Chat Logs (Full Audio Analysis) ← YOU WANT THIS
```
INFO - Transcribing audio for session session-123
INFO - Transcription complete in 1200ms: I'm feeling really anxious today
INFO - Analyzing audio features
INFO - 📊 Speaker baseline: pitch=180.5Hz, amplitude=0.045
INFO - 🎵 Word 'I'm': pitch=0.52, amp=0.48, stressed=False, hint=neutral
INFO - 🎵 Word 'feeling': pitch=0.55, amp=0.51, stressed=False, hint=neutral
INFO - 🎵 Word 'really': pitch=0.68, amp=0.72, stressed=True, hint=anxiety
INFO - 🎵 Word 'anxious': pitch=0.75, amp=0.78, stressed=True, hint=anxiety
INFO - ✓ Analyzed 6 words from audio
INFO - ✓ Computed text weights for 6 words
INFO - Running fusion engine
INFO - 🎯 Text-only emotion: fear (0.82)
INFO - 🎵 Audio-focused emotion: fear (0.91)
INFO - ⚡ FUSED emotion: fear (0.88)
INFO - 💪 Stressed words: really, anxious
INFO: POST /api/voice/chat HTTP/1.1 200 OK
```

## Frontend Response Comparison

### Text Chat Response
```
User: I'm feeling anxious

Bot: I hear that you're feeling anxious...

[emotion: fear 82%] [intent: anxiety and panic] [lang: en] [450ms]
```

### Voice Chat Response ← YOU WANT THIS
```
User: 🎤 I'm feeling really anxious today

Bot: I hear that you're feeling anxious...

[🎤 voice] [emotion: fear 88%] [text: fear 82%] [audio: anxiety 91%]
[duration: 3.2s] [processing: 2450ms]

Emphasized words: really, anxious
```

## How to Test RIGHT NOW

### Step 1: Keep Backend Running ✅
You already have it running!

### Step 2: Open Frontend
```bash
start mental_health_chatbot/frontend_test/index.html
```

### Step 3: Click 🎤 (NOT the text box!)
```
DO THIS:
  Click [🎤] → Speak → Click [⏹️]

NOT THIS:
  Type in box → Press Enter
```

### Step 4: Watch Backend Terminal
Look for these specific log lines:
- ✅ "Transcribing audio for session..."
- ✅ "📊 Speaker baseline: pitch=..."
- ✅ "🎵 Word '...': pitch=..."
- ✅ "🎯 Text-only emotion: ..."
- ✅ "🎵 Audio-focused emotion: ..."
- ✅ "⚡ FUSED emotion: ..."

If you see these, **IT'S WORKING!** 🎉

## Quick Checklist

Before testing:
- [ ] Backend is running
- [ ] You see "✓ Whisper model loaded"
- [ ] You see "✓ ffmpeg is available"
- [ ] Frontend is open in browser
- [ ] You clicked 🎤 (not typed in text box)
- [ ] You allowed microphone permissions
- [ ] You spoke clearly for 2-3 seconds
- [ ] You clicked ⏹️ to stop

After testing:
- [ ] Backend shows "Transcribing audio..."
- [ ] Backend shows "📊 Speaker baseline..."
- [ ] Backend shows "🎯 Text-only emotion..."
- [ ] Backend shows "🎵 Audio-focused emotion..."
- [ ] Backend shows "⚡ FUSED emotion..."
- [ ] Frontend shows 🎤 icon in user message
- [ ] Frontend shows voice metadata

## Still Not Working?

### Test with curl (bypass frontend)
```bash
# Record a test audio file first, then:
curl -X POST http://localhost:8000/api/voice/chat \
  -F "session_id=test123" \
  -F "audio=@test.wav" \
  -v
```

Watch backend logs - you should see all the audio analysis!

### Check Browser Console
Press F12 in browser, look for errors in Console tab.

### Verify Microphone Works
Try recording in Windows Voice Recorder first to confirm mic works.

## Summary

**You tested:** Typing → Text endpoint → No audio analysis ❌
**You need:** Microphone → Voice endpoint → Full audio analysis ✅

**The feature IS implemented and working - you just need to use the 🎤 button!**
