# Voice Pipeline Integration - React Frontend

## ✅ What Was Added

The React frontend now has **full voice pipeline integration** with audio-fused emotion detection!

## 🎤 Two Voice Buttons

You now have TWO voice input options:

### 1. 🎤 Mic Button (Voice-to-Text)
- **What it does**: Browser speech recognition → converts speech to text
- **Processing**: Client-side only (no backend)
- **Use case**: Quick text input via voice
- **No emotion analysis**

### 2. 🌊 Waves Button (Voice Pipeline - NEW!)
- **What it does**: Records audio → sends to backend → full audio analysis
- **Processing**: Backend analyzes pitch, amplitude, stress patterns
- **Use case**: Emotion-aware conversations
- **Shows**: Fused emotion, text vs audio comparison, stressed words, incongruence detection

## 🚀 How to Use

### Step 1: Start Backend
```bash
cd mental_health_chatbot/backend
python main.py
```

Wait for:
```
✓ Whisper model loaded
✓ ffmpeg is available
```

### Step 2: Start React Frontend
```bash
cd react_web
npm run dev
```

### Step 3: Use Voice Pipeline
1. Open the chat page
2. Click the **🌊 Waves button** (next to mic button)
3. Allow microphone access
4. Speak clearly: "I'm feeling really anxious today"
5. Click **Stop** when done
6. Wait 2-4 seconds for processing

### Step 4: See Voice Analysis
The bot response will show:
```
[Bot response text]

🎤 Voice Analysis
Fused Emotion: fear (88%)
Text: fear (82%)
Audio: anxiety (91%)
Emphasized: really, anxious

⚠️ [Incongruence note if detected]
```

## 📊 What You'll See

### User Message
```
🎤 I'm feeling really anxious today
```

### Bot Response with Voice Analysis
```
I hear that you're feeling anxious. That must be difficult...

🎤 Voice Analysis
├─ Fused Emotion: fear (88%)
├─ Text: fear (82%)
├─ Audio: anxiety (91%)
└─ Emphasized: really, anxious
```

### If Incongruence Detected
```
⚠️ Your words suggest neutral but your voice patterns suggest 
anxiety. This contrast can sometimes indicate masked distress.
```

## 🔍 Backend Logs

When you use the voice pipeline, watch the backend terminal:

```
INFO - Transcribing audio for session...
INFO - 📊 Speaker baseline: pitch=180.5Hz, amplitude=0.045
INFO - 🎵 Word 'really': pitch=0.68, amp=0.72, stressed=True, hint=anxiety
INFO - ✓ Analyzed 6 words from audio
INFO - 🎯 Text-only emotion: fear (0.82)
INFO - 🎵 Audio-focused emotion: fear (0.91)
INFO - ⚡ FUSED emotion: fear (0.88)
INFO - 💪 Stressed words: really, anxious
```

## 🎯 Files Modified

### New Files
1. `src/components/chat/VoicePipelineInput.jsx` - Voice recording component
2. `src/components/chat/VoiceInput.css` - Added voice pipeline styles

### Modified Files
1. `src/components/chat/ChatInput.jsx` - Added voice pipeline button
2. `src/pages/MentalHealthChatPage.jsx` - Added voice result handler
3. `src/components/chat/MessageBubble.jsx` - Added voice analysis display
4. `src/styles/MentalHealthChat.css` - Added voice analysis styles

## 🧪 Testing

### Test 1: Normal Emotion
Say: "I'm feeling really anxious today"
- **Expected**: High confidence, text and audio agree

### Test 2: Incongruence
Say: "I'm fine" in a SAD voice
- **Expected**: Incongruence warning, text says neutral/joy but audio says sadness

### Test 3: Stressed Words
Say: "I'm REALLY, REALLY anxious" (emphasize "really")
- **Expected**: "really" appears in emphasized words

## 🐛 Troubleshooting

### "Could not access microphone"
- Check browser permissions (click 🔒 in address bar)
- Make sure no other app is using the microphone
- Try refreshing the page

### "Error processing voice"
- Check if backend is running
- Check backend logs for errors
- Verify ffmpeg is in PATH: `ffmpeg -version`
- Check `/api/voice/health` endpoint

### No voice analysis shown
- Make sure you clicked the **🌊 Waves button**, not the 🎤 mic button
- Check browser console (F12) for errors
- Check backend logs for processing

### Backend shows "POST /api/chat" instead of "/api/voice/chat"
- You're using the wrong button! Use 🌊 Waves, not 🎤 Mic

## 💡 Tips

### For Best Results
- Speak clearly and naturally
- 2-5 seconds is ideal length
- Express emotion naturally (the system detects it!)
- Avoid background noise

### Test Phrases
- "I'm feeling really anxious today" (clear emotion)
- "I'm fine" (said sadly - tests incongruence)
- "Nobody understands me" (loneliness)
- "I can't handle this anymore" (stress)

## 🎨 UI Features

### Voice Pipeline Button
- Has "AI" badge to distinguish from regular mic
- Tooltip: "Voice with emotion analysis"
- Located next to the mic button

### Voice Analysis Display
- Shows in bot message bubble
- Purple accent color
- Grid layout for emotions
- Incongruence warning in red

### Recording UI
- Waveform visualization
- Timer display
- Stop button
- Processing indicator

## 📝 Technical Details

### Audio Format
- Recorded as: `audio/webm`
- Sent to: `POST /api/voice/chat`
- Processed by: Whisper + librosa + fusion engine

### Processing Flow
1. Record audio in browser
2. Send to backend as multipart/form-data
3. Backend transcribes with Whisper
4. Analyzes audio features with librosa
5. Computes text weights
6. Fuses audio + text emotions
7. Returns full analysis to frontend
8. Frontend displays voice metadata

### Performance
- Recording: instant
- Upload: <100ms (local)
- Processing: 2-4 seconds
- Total: ~3-5 seconds

## ✅ Success Checklist

- [ ] Backend running with Whisper loaded
- [ ] ffmpeg available in PATH
- [ ] React frontend running
- [ ] Clicked 🌊 Waves button (not 🎤)
- [ ] Allowed microphone permissions
- [ ] Spoke for 2-3 seconds
- [ ] Clicked Stop
- [ ] Saw voice analysis in bot response
- [ ] Backend logs show audio analysis

## 🎉 You're Ready!

The voice pipeline is fully integrated! Click the **🌊 Waves button** and start testing emotion-aware conversations!
