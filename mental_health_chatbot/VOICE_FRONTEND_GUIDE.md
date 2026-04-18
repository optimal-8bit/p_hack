# Voice Feature - Frontend Guide

## What Was Added

The existing frontend test UI now has **microphone support** integrated with the voice pipeline backend.

## New Features

### 🎤 Microphone Button
- Click the microphone button (🎤) to start recording
- Button turns red and shows stop icon (⏹️) while recording
- Click again to stop and send the audio

### Voice Indicator
- Shows "Recording..." while capturing audio
- Shows "Processing audio..." while sending to backend
- Automatically hides when done

### Enhanced Response Display
- Transcript shown as user message with 🎤 icon
- Bot response includes voice-specific metadata:
  - **Fused emotion** (combined text + audio)
  - **Text-only emotion** (what the words say)
  - **Audio-focused emotion** (what the voice sounds like)
  - **Audio duration** and processing time
  - **Stressed words** (emotionally important words)
  - **Incongruence warning** (if words contradict voice)

## How to Use

### 1. Fix ffmpeg PATH First

**Quick fix (temporary):**
```powershell
$env:PATH += ";C:\ffmpeg\bin"
ffmpeg -version
```

**Permanent fix:**
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "User")
```

Then **restart PowerShell** and verify:
```powershell
ffmpeg -version
python test_voice_imports.py
```

### 2. Start the Backend

```bash
cd mental_health_chatbot/backend
python main.py
```

Wait for:
```
✓ Whisper model loaded successfully
✓ ffmpeg is available
```

### 3. Open the Frontend

```bash
# Open in browser
start mental_health_chatbot/frontend_test/index.html

# Or just double-click index.html
```

### 4. Test Voice Input

1. Click the **🎤 microphone button**
2. Allow microphone access when prompted
3. Speak your message (e.g., "I'm feeling anxious today")
4. Click **⏹️ stop button** when done
5. Wait for processing (2-4 seconds)
6. See your transcript and bot response with voice analysis

## What You'll See

### User Message
```
🎤 I'm feeling really anxious today
```

### Bot Response with Voice Metadata
```
I hear that you're feeling anxious. That must be difficult...

[🎤 voice] [emotion: fear 88%] [text: fear 82%] [audio: anxiety 91%]
[duration: 3.2s] [processing: 2450ms]

Emphasized words: really, anxious
```

### If Incongruence Detected
```
⚠️ Note: Your words suggest neutral but your voice patterns suggest 
anxiety. This contrast can sometimes indicate masked distress.
```

## Browser Compatibility

### ✅ Supported Browsers
- Chrome/Edge (recommended)
- Firefox
- Safari (macOS/iOS)
- Opera

### ⚠️ Requirements
- HTTPS or localhost (for microphone access)
- Microphone permissions granted
- Modern browser (supports MediaRecorder API)

## Troubleshooting

### "Microphone access denied"
- Click the 🔒 lock icon in browser address bar
- Allow microphone access
- Refresh the page

### "Could not access microphone"
- Check if another app is using the microphone
- Check browser permissions
- Try a different browser

### "Error processing voice"
- Check if backend is running (`python main.py`)
- Check if ffmpeg is in PATH (`ffmpeg -version`)
- Check browser console (F12) for detailed errors
- Try recording again

### No response after recording
- Check backend logs for errors
- Verify `/api/voice/health` shows all green
- Try with a longer recording (2-3 seconds minimum)

### "ffmpeg binary not found"
See `FIX_FFMPEG_PATH.md` for detailed instructions.

## Testing Tips

### Good Test Phrases
- "I'm feeling really anxious today" (clear emotion)
- "I'm fine" (said in sad voice - tests incongruence)
- "I can't handle this anymore" (high stress)
- "Nobody understands me" (loneliness)

### Recording Tips
- Speak clearly and naturally
- 2-5 seconds is ideal length
- Avoid background noise
- Express emotion naturally (the system detects it!)

## Technical Details

### Audio Format
- Recorded as: `audio/webm` (browser default)
- Sent to: `POST /api/voice/chat`
- Converted by: ffmpeg (backend)
- Transcribed by: Whisper (backend)

### Processing Flow
1. Browser records audio → webm blob
2. Sent to backend via multipart/form-data
3. Backend transcribes with Whisper
4. Analyzes audio features with librosa
5. Fuses text + audio emotions
6. Generates response
7. Returns full analysis to frontend

### Performance
- Recording: instant
- Upload: <100ms (local)
- Processing: 2-4 seconds
- Total: ~3-5 seconds

## Advanced Features

### Emotion Fusion
The system runs emotion detection **twice**:
1. On full transcript text
2. On high-weight words only (emotionally important)

Then fuses with audio features for final emotion.

### Incongruence Detection
Compares what you **say** vs how you **sound**:
- Words: "I'm fine" → neutral
- Voice: low pitch, quiet → sadness
- Result: **Incongruent** → flags potential masked distress

### Stressed Words
Words with high combined importance (text + audio):
- High text weight: emotional vocabulary
- High audio weight: pitch/amplitude spikes
- Combined: truly emphasized words

## Next Steps

1. **Fix ffmpeg PATH** (see `FIX_FFMPEG_PATH.md`)
2. **Test the feature** with various emotions
3. **Check voice health**: http://localhost:8000/api/voice/health
4. **View API docs**: http://localhost:8000/docs

## Files Modified

- `frontend_test/index.html` - Added mic button and voice indicator
- `frontend_test/app.js` - Added voice recording and API integration

## Support

If you encounter issues:
1. Check backend logs in terminal
2. Check browser console (F12)
3. Verify ffmpeg: `ffmpeg -version`
4. Test voice health: `curl http://localhost:8000/api/voice/health`
5. Try text chat first to verify backend works
