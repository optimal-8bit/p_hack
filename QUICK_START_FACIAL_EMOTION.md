# Quick Start: Facial Emotion Detection

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Backend
```bash
cd mental_health_chatbot/backend
python main.py
```

Backend runs at: `http://localhost:8000`

### Step 2: Start the Frontend
```bash
cd react_web
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Step 3: Enable Webcam Emotion Detection

1. Open `http://localhost:5173` in your browser
2. Navigate to the chat interface
3. Click the **camera button** (📷) in the top-right area
4. **Grant camera permission** when prompted
5. Wait for models to load (progress bar: 1/4 → 2/4 → 3/4 → 4/4)
6. Webcam starts with live emotion detection! 🎉

## 💬 Testing the Feature

### Test 1: Congruent Emotions
1. **Smile** at the camera 😊
2. Type: "I'm feeling really happy today!"
3. Send the message
4. Bot response will show: **✓ Emotions align**

### Test 2: Incongruent Emotions (The Magic!)
1. Make a **sad face** 😢
2. Type: "I'm fine, everything is okay"
3. Send the message
4. Bot response will show: **⚠️ Emotional incongruence detected**
5. This is the killer feature for mental health support!

### Test 3: Disable Webcam
1. Click the **close button** (✕) on the webcam display
2. Or click the camera toggle button again
3. Chat continues with text-only emotion detection

## 🎯 What You'll See

### User Message
```
┌─────────────────────────────────┐
│ 😊 happy 95%                    │ ← Facial emotion badge
│                                 │
│ I'm feeling great today!        │
└─────────────────────────────────┘
```

### Bot Response (Multimodal Analysis)
```
┌─────────────────────────────────┐
│ That's wonderful to hear!       │
│                                 │
│ 🧠 Emotion Analysis             │
│ ├─ Text Emotion: 😊 joy         │
│ ├─ Facial Emotion: 😊 happy     │
│ └─ Congruence: ✓ Emotions align │
└─────────────────────────────────┘
```

### Incongruence Detection
```
┌─────────────────────────────────┐
│ I hear you saying you're fine,  │
│ but I sense you might be        │
│ feeling differently. Would you  │
│ like to talk about it?          │
│                                 │
│ 🧠 Emotion Analysis             │
│ ├─ Text Emotion: 😐 neutral     │
│ ├─ Facial Emotion: 😢 sad       │
│ └─ Congruence: ⚠️ Incongruent   │
└─────────────────────────────────┘
```

## 🔧 Troubleshooting

### Camera Permission Denied
- Click the camera icon in browser address bar
- Allow camera access
- Refresh the page

### Models Not Loading
- Check internet connection (models load from CDN)
- Wait a few seconds and try again
- Check browser console for errors

### No Face Detected
- Ensure good lighting 💡
- Face the camera directly
- Move closer to the camera
- Remove obstructions (masks, hands)

### Webcam Already in Use
- Close other apps using the camera (Zoom, Teams, etc.)
- Refresh the browser tab

## 📊 Technical Details

### What Gets Sent to Backend
Only emotion metadata (no video/images):
```json
{
  "dominant_emotion": "happy",
  "confidence": 0.95,
  "age": 27,
  "gender": "female"
}
```

### Privacy Guarantees
- ✅ 100% client-side detection
- ✅ No video upload
- ✅ No image capture
- ✅ No recording
- ✅ User control (can disable anytime)

## 🎨 UI Elements

### Webcam Display
- **Location**: Top-right corner
- **Size**: Compact (200px)
- **Features**:
  - Live video feed (mirrored)
  - Emotion badge overlay
  - Colored bounding box around face
  - Close button

### Toggle Button
- **Icon**: 📷 (off) / 📹 (on)
- **Location**: Next to webcam
- **Color**: Blue when active

### Message Badges
- **User messages**: Show detected facial emotion
- **Bot responses**: Show multimodal analysis

## 🚨 Important Notes

1. **HTTPS Required in Production**: Browsers require HTTPS for webcam access (except localhost)
2. **First Load is Slower**: Models download on first use (~6MB, then cached)
3. **CPU Usage**: Minimal impact (optimized models)
4. **Browser Support**: Chrome, Firefox, Safari (modern versions)

## 🎓 Advanced Usage

### Combining with Voice Input
1. Enable webcam emotion detection
2. Use voice input feature (microphone button)
3. Get **triple-modal analysis**:
   - Text emotion (from transcript)
   - Audio emotion (from voice prosody)
   - Facial emotion (from webcam)

### Emotion History
- Facial emotion is captured at the moment you send the message
- Each message stores its own facial emotion snapshot
- Scroll through conversation to see emotion changes over time

## 📝 Example Conversation

```
User (😊 happy 92%): "I got the job!"
Bot: Congratulations! That's fantastic news! 
     [✓ Emotions align - genuine happiness detected]

User (😢 sad 88%): "But I'm worried about moving"
Bot: It's completely normal to feel anxious about 
     big changes. Let's talk about your concerns.
     [✓ Emotions align - acknowledging mixed feelings]

User (😐 neutral 65%): "I'm fine with it"
Bot: I notice some hesitation. It's okay to have 
     mixed feelings about this transition.
     [⚠️ Incongruent - text says fine, face shows concern]
```

## 🎉 Success!

You now have a **multimodal emotion detection system** running! The chatbot can:
- Detect emotions from text, voice, AND facial expressions
- Identify when someone is hiding their true feelings
- Provide more empathetic and accurate responses
- Help users feel truly understood

## 📚 Next Steps

- Read `FACIAL_EMOTION_INTEGRATION.md` for technical details
- Explore emotion fusion logic in `backend/models/emotion_fusion.py`
- Customize emotion detection thresholds
- Add emotion history visualization
- Integrate with therapist dashboard

---

**Need Help?** Check the troubleshooting section or review the full documentation in `FACIAL_EMOTION_INTEGRATION.md`
