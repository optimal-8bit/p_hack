# Voice Pipeline with Audio-Fused Emotion Detection

## Overview

This feature adds voice input capability to the mental health chatbot with **audio-fused emotion detection**. Instead of just transcribing audio and analyzing text, it combines acoustic features (pitch, amplitude, stress patterns) with text analysis to produce more accurate emotion detection.

## Key Features

### 1. Two-Stage Emotion Fusion
- **Stage 1**: Analyze full transcript text for emotion
- **Stage 2**: Extract high-weight words (emotionally important) and re-analyze
- **Stage 3**: Fuse both results with audio features for final emotion

### 2. Emotional Incongruence Detection
Detects when someone's words contradict their voice patterns (e.g., saying "I'm fine" in a distressed voice). This is a clinically meaningful signal that can indicate masked distress.

### 3. Per-Word Audio Analysis
Each word is analyzed for:
- Pitch (normalized to speaker baseline)
- Amplitude/volume
- Stress patterns
- Emotion hints (anxiety, sadness, anger, dissociation, neutral)

### 4. Text Attribution
Computes importance of each word using:
- **Leave-one-out** for short messages (≤15 words)
- **Vocabulary lookup** for longer messages (>15 words)

## Architecture

```
Audio File
    ↓
[Transcriber] → Whisper model → transcript + word timestamps
    ↓
[Safety Check] → Crisis detection on transcript
    ↓
[Audio Analyzer] → librosa → per-word audio features
    ↓
[Word Attributor] → text importance weights
    ↓
[Fusion Engine] → combine audio + text → fused emotion
    ↓
[Orchestrator] → generate response with fused emotion
    ↓
Response
```

## New Files Created

### Voice Module (`backend/voice/`)
- `transcriber.py` - Whisper-based transcription with word timestamps
- `audio_analyzer.py` - librosa-based audio feature extraction
- `word_attributor.py` - Text importance computation
- `fusion_engine.py` - Audio-text fusion logic
- `voice_pipeline.py` - Main coordinator
- `voice_routes.py` - FastAPI endpoints

### Modified Files
- `main.py` - Added voice router registration, Whisper pre-loading, ffmpeg check
- `api/routes.py` - Added voice_pipeline_loaded to health endpoint
- `api/schemas.py` - Added VoiceChatResponseSchema and FusedWordResultSchema
- `pipeline/orchestrator.py` - Added override_emotion parameter (optional, only used by voice pipeline)
- `requirements.txt` - Added voice dependencies

## Installation

### 1. Install Python Dependencies

```bash
cd mental_health_chatbot/backend
pip install -r requirements.txt
```

New dependencies:
- `openai-whisper==20231117` - Speech-to-text
- `librosa==0.10.1` - Audio analysis
- `soundfile==0.12.1` - Audio I/O
- `ffmpeg-python==0.2.0` - Audio format conversion

### 2. Install ffmpeg (System-Level)

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 3. First Run

On first startup, Whisper will download the "small" model (~460MB). This happens automatically.

```bash
python main.py
```

Check logs for:
```
✓ Whisper model loaded successfully
✓ ffmpeg is available
```

## API Endpoints

### POST /api/voice/chat

Process voice message with audio-fused emotion detection.

**Request:**
- Content-Type: `multipart/form-data`
- `session_id` (form field): Session identifier
- `audio` (file): Audio file

**Supported Formats:** `.wav`, `.mp3`, `.m4a`, `.webm`, `.ogg`  
**Max File Size:** 10MB

**Response:**
```json
{
  "transcript": "I feel really anxious today",
  "detected_language": "en",
  "audio_duration_seconds": 3.2,
  "transcription_time_ms": 1200,
  "fusion_time_ms": 450,
  
  "text_only_emotion": "fear",
  "text_only_confidence": 0.82,
  "audio_focused_emotion": "fear",
  "audio_focused_confidence": 0.91,
  "fused_emotion": "fear",
  "fused_confidence": 0.88,
  
  "intent": "anxiety and panic",
  "intent_confidence": 0.89,
  
  "is_incongruent": false,
  "incongruence_score": 0.1,
  "incongruence_note": "",
  
  "word_analysis": [
    {
      "word": "anxious",
      "final_weight": 0.85,
      "text_weight": 0.90,
      "audio_weight": 0.80,
      "pitch_normalized": 0.72,
      "amplitude_normalized": 0.68,
      "is_stressed": true,
      "emotion_hint": "anxiety"
    }
  ],
  "stressed_words": ["really", "anxious"],
  
  "chat_result": {
    "response_text": "I hear that you're feeling anxious...",
    "detected_language": "en",
    "emotion": {...},
    "intent": {...},
    "turn_number": 1,
    "is_crisis": false,
    "processing_time_ms": 2500,
    "session_id": "user123"
  }
}
```

### GET /api/voice/health

Check voice pipeline status.

**Response:**
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

## Testing

### Using curl

```bash
# Test voice chat
curl -X POST http://localhost:8000/api/voice/chat \
  -F "session_id=test123" \
  -F "audio=@test_audio.wav"

# Check voice health
curl http://localhost:8000/api/voice/health
```

### Using Python

```python
import requests

# Voice chat
with open("test_audio.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/voice/chat",
        data={"session_id": "test123"},
        files={"audio": f}
    )
    print(response.json())
```

## How It Works

### 1. Transcription
Whisper transcribes audio and extracts word-level timestamps. If word timestamps are missing, they're estimated from segment timings.

### 2. Audio Analysis
For each word:
- Extract pitch using YIN algorithm (50-400 Hz range)
- Extract amplitude using RMS energy
- Normalize to speaker baseline (computed from full clip)
- Calculate stress indicators
- Assign emotion hint based on acoustic patterns

### 3. Text Attribution
**Short messages (≤15 words):**
- Run emotion model on full text → baseline confidence
- For each word, remove it and re-run → confidence drop = importance

**Long messages (>15 words):**
- Use vocabulary lookup (HIGH_EMOTION_WORDS, MEDIUM_EMOTION_WORDS)
- Avoids 15+ model calls

### 4. Fusion
- Combine text_weight (50%) + audio_weight (50%) = final_weight
- Extract high-weight words (final_weight > 0.55)
- Run emotion model on high-weight words only
- Fuse with full-text emotion:
  - If agree: weighted average (40% text, 60% audio-focused)
  - If disagree: pick higher confidence, apply 15% penalty

### 5. Incongruence Detection
- Map emotions to valence: negative (-1), positive (+1), neutral (0)
- Compare text emotion vs dominant audio emotion
- If valence difference > 0.4: flag as incongruent
- Generate human-readable note

## Clinical Significance

### Emotional Incongruence
When someone says "I'm fine" but their voice shows distress patterns (low pitch, low amplitude, flat affect), this mismatch is clinically meaningful. It can indicate:
- Emotional suppression
- Alexithymia (difficulty identifying emotions)
- Social masking
- Dissociation

The system flags this and provides a gentle note to the user.

### Dissociation Detection
Flat affect (low amplitude + low pitch deviation) is detected as "dissociation" emotion hint. This is important for mental health assessment.

## Performance

**Typical Processing Times (CPU):**
- Transcription: 1-2 seconds per 3-second audio clip
- Audio analysis: 200-400ms
- Fusion: 100-200ms
- Total: 1.5-3 seconds

**First Run:**
- Whisper model download: ~460MB, one-time
- First transcription: +5-10 seconds (model warmup)

## Limitations

1. **CPU-Only**: Designed for CPU inference. GPU would be faster but not required.
2. **English-Optimized**: Whisper supports many languages, but emotion hints are tuned for English speech patterns.
3. **Audio Quality**: Works best with clear speech. Background noise may affect accuracy.
4. **Short Clips**: Optimized for 1-10 second clips. Very long audio may be slow.

## Troubleshooting

### "Whisper model not loaded"
- Check internet connection (first run downloads model)
- Check disk space (~500MB needed)
- Check logs for detailed error

### "ffmpeg not found"
- Install ffmpeg system-wide (see Installation section)
- Only .wav will work without ffmpeg
- Check with: `ffmpeg -version`

### "librosa failed to analyze word"
- Usually due to very short word segments or silence
- System falls back to safe defaults automatically
- Not a critical error

### Empty transcript
- Check audio file is not corrupted
- Ensure audio contains speech
- Try different audio format

## Future Enhancements

Possible improvements:
- GPU acceleration for faster processing
- Streaming audio support
- Real-time emotion tracking
- Multi-speaker detection
- Emotion trajectory visualization
- Fine-tuned emotion hints for non-English languages

## Integration Notes

### Existing Text Chat Unaffected
The voice pipeline is completely isolated. The existing `POST /api/chat` endpoint works exactly as before. The only change to the orchestrator is an optional `override_emotion` parameter that is only used when called from the voice pipeline.

### Database Integration
Voice messages are saved to the database through the orchestrator's existing flow. The transcript is stored as the user message.

### Crisis Detection
Crisis patterns are checked on the transcript text before any audio analysis. If crisis is detected, the system returns immediately with crisis resources.

## Code Quality

- All modules follow existing singleton patterns
- Error handling at every step with graceful fallbacks
- Temporary files cleaned up in finally blocks
- Comprehensive logging for debugging
- Type hints and docstrings throughout
- No breaking changes to existing code
