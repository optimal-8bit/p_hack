# 🧪 Facial Emotion Detection - Testing Guide

## Overview

This guide provides comprehensive testing procedures for the facial emotion detection feature, including debugging tools and troubleshooting steps.

## 🚀 Quick Start Testing

### 1. Backend API Test (Python Script)
```bash
# Make sure backend is running first
cd mental_health_chatbot/backend
python main.py

# In another terminal, run the test script
python test_facial_emotion_quick.py
```

**Expected Output:**
```
[10:30:15] ℹ️ Starting facial emotion detection backend tests...
[10:30:15] ✅ Backend is healthy: healthy
[10:30:16] ✅ Text-only chat successful
[10:30:17] ✅ Multimodal congruent test successful
[10:30:18] ✅ Multimodal incongruent test successful
[10:30:19] ✅ Edge case test successful
[10:30:20] 🎉 ALL TESTS PASSED (5/5)
```

### 2. Frontend Component Test (HTML Page)
```bash
# Open the test page in your browser
open test_facial_emotion.html
# or
start test_facial_emotion.html
```

**Test Steps:**
1. Wait for models to load (progress bar: 0/4 → 4/4)
2. Click "Start Webcam"
3. Grant camera permission
4. Verify video preview appears
5. Try different facial expressions
6. Check emotion detection accuracy
7. Test backend integration button

### 3. Full Integration Test (React App)
```bash
# Start backend
cd mental_health_chatbot/backend
python main.py

# Start frontend
cd react_web
npm run dev

# Open http://localhost:5173
# Navigate to chat
# Click camera button (📷)
# Test facial emotion detection in chat
```

## 📋 Detailed Testing Procedures

### Backend Testing

#### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "emotion_classifier": true,
    "intent_classifier": true,
    "voice_pipeline_loaded": true
  },
  "version": "1.0.0"
}
```

#### Test 2: Text-Only Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "message": "I am feeling happy today"
  }'
```

**Expected Response:**
```json
{
  "response_text": "That's wonderful to hear!...",
  "emotion": {
    "emotion": "joy",
    "confidence": 0.85,
    "is_multimodal": false,
    "emotion_congruence": null
  }
}
```

#### Test 3: Multimodal Chat (Congruent)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "message": "I am feeling happy today",
    "facial_emotion": {
      "dominant_emotion": "happy",
      "confidence": 0.95,
      "all_emotions": {"happy": 0.95, "neutral": 0.05},
      "age": 27,
      "gender": "female"
    }
  }'
```

**Expected Response:**
```json
{
  "emotion": {
    "emotion": "joy",
    "confidence": 0.92,
    "facial_emotion": "happy",
    "facial_confidence": 0.95,
    "is_multimodal": true,
    "emotion_congruence": "congruent"
  }
}
```

#### Test 4: Multimodal Chat (Incongruent)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "message": "I am fine, everything is okay",
    "facial_emotion": {
      "dominant_emotion": "sad",
      "confidence": 0.87,
      "all_emotions": {"sad": 0.87, "neutral": 0.13}
    }
  }'
```

**Expected Response:**
```json
{
  "emotion": {
    "emotion": "sadness",
    "confidence": 0.87,
    "facial_emotion": "sad",
    "facial_confidence": 0.87,
    "is_multimodal": true,
    "emotion_congruence": "incongruent"
  }
}
```

### Frontend Testing

#### Test 1: Model Loading
1. Open browser developer tools (F12)
2. Go to Console tab
3. Open the chat page
4. Click camera button
5. Watch for loading logs:

```
🚀 [FACIAL-EMOTION] Starting model loading...
📥 [FACIAL-EMOTION] Loading SSD MobileNet v1 (1/4)...
✅ [FACIAL-EMOTION] SSD MobileNet v1 loaded
📥 [FACIAL-EMOTION] Loading Face Landmark 68 (2/4)...
✅ [FACIAL-EMOTION] Face Landmark 68 loaded
📥 [FACIAL-EMOTION] Loading Face Expression Net (3/4)...
✅ [FACIAL-EMOTION] Face Expression Net loaded
📥 [FACIAL-EMOTION] Loading Age Gender Net (4/4)...
✅ [FACIAL-EMOTION] Age Gender Net loaded
🎉 [FACIAL-EMOTION] All models loaded successfully! Ready for detection.
```

#### Test 2: Webcam Access
Watch for webcam logs:

```
📹 [FACIAL-EMOTION] Requesting webcam access...
✅ [FACIAL-EMOTION] Webcam access granted
📊 [FACIAL-EMOTION] Video stream info: {tracks: 1, settings: {...}}
📺 [FACIAL-EMOTION] Video metadata loaded: {width: 640, height: 480}
▶️ [FACIAL-EMOTION] Video can play, starting playback...
🎬 [FACIAL-EMOTION] Video playback started
🎥 [FACIAL-EMOTION] Webcam started successfully
```

#### Test 3: Emotion Detection
Watch for detection logs:

```
🎯 [FACIAL-EMOTION] Starting emotion detection loop (500ms interval)...
✅ [FACIAL-EMOTION] Emotion detection started
😊 [FACIAL-EMOTION] Face detected: {emotion: "happy", confidence: "95.2%", age: 27, gender: "female"}
```

#### Test 4: Message Sending
Watch for chat logs:

```
💬 [CHAT] Sending message: {message: "I'm happy", hasFacialEmotion: true, facialEmotion: "happy"}
📤 [WEBCAM-COMPONENT] Sending emotion to parent: {dominant_emotion: "happy", confidence: 0.95}
✅ [CHAT] Message completed: {emotionAnalysis: {...}, isMultimodal: true, congruence: "congruent"}
```

## 🔍 Debugging Common Issues

### Issue 1: Models Not Loading

**Symptoms:**
- Progress bar stuck at 0/4
- Error: "Failed to load emotion detection models"

**Debug Steps:**
1. Check internet connection
2. Check browser console for network errors
3. Verify CDN accessibility:
   ```bash
   curl -I https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.12/model/ssd_mobilenetv1_model-weights_manifest.json
   ```

**Solutions:**
- Refresh the page
- Try a different browser
- Check firewall/proxy settings
- Use a different CDN or host models locally

### Issue 2: Webcam Not Starting

**Symptoms:**
- Black video area
- Error: "Failed to access webcam"

**Debug Steps:**
1. Check camera permissions in browser
2. Verify camera is not used by another app
3. Check browser console for specific error:
   - `NotAllowedError`: Permission denied
   - `NotFoundError`: No camera found
   - `NotReadableError`: Camera in use

**Solutions:**
- Grant camera permission
- Close other apps using camera
- Try different browser
- Check camera drivers

### Issue 3: No Face Detected

**Symptoms:**
- Video shows but no bounding box
- "No face detected" message

**Debug Steps:**
1. Check lighting conditions
2. Verify face is in frame
3. Check detection logs for errors
4. Test with different face positions

**Solutions:**
- Improve lighting
- Move closer to camera
- Face camera directly
- Remove obstructions (masks, hands)

### Issue 4: Video Preview Not Visible

**Symptoms:**
- Black box instead of video
- Canvas overlay visible but no video

**Debug Steps:**
1. Check video element properties:
   ```javascript
   console.log('Video ready state:', videoRef.current.readyState);
   console.log('Video dimensions:', videoRef.current.videoWidth, videoRef.current.videoHeight);
   console.log('Video src object:', videoRef.current.srcObject);
   ```

2. Check CSS styling:
   ```javascript
   console.log('Video display:', getComputedStyle(videoRef.current).display);
   console.log('Video visibility:', getComputedStyle(videoRef.current).visibility);
   ```

**Solutions:**
- Ensure video has `autoplay` attribute
- Check CSS `display` and `visibility` properties
- Verify video stream is active
- Try different video constraints

### Issue 5: Backend Integration Failing

**Symptoms:**
- Facial emotion not sent to backend
- No multimodal analysis in response

**Debug Steps:**
1. Check network requests in browser dev tools
2. Verify request payload includes `facial_emotion`
3. Check backend logs for emotion fusion messages
4. Test backend directly with curl

**Solutions:**
- Verify backend is running
- Check CORS configuration
- Ensure facial emotion data is captured
- Validate request format

## 📊 Performance Testing

### Metrics to Monitor

1. **Model Load Time**
   - Target: < 5 seconds
   - Measure: Time from start to "All models loaded"

2. **Detection Frequency**
   - Target: 2 FPS (every 500ms)
   - Measure: Time between detection logs

3. **Detection Accuracy**
   - Target: > 80% for clear expressions
   - Measure: Manual verification of detected emotions

4. **Memory Usage**
   - Target: < 100MB additional
   - Measure: Browser task manager

5. **CPU Usage**
   - Target: < 20% additional
   - Measure: Browser task manager

### Performance Test Script

```javascript
// Run in browser console
let detectionCount = 0;
let startTime = Date.now();

// Override console.log to count detections
const originalLog = console.log;
console.log = function(...args) {
  if (args[0] && args[0].includes('[FACIAL-EMOTION] Face detected:')) {
    detectionCount++;
    const elapsed = (Date.now() - startTime) / 1000;
    const fps = detectionCount / elapsed;
    console.info(`Detection FPS: ${fps.toFixed(2)}`);
  }
  originalLog.apply(console, args);
};

// Reset after 30 seconds
setTimeout(() => {
  console.log = originalLog;
  const elapsed = (Date.now() - startTime) / 1000;
  const avgFps = detectionCount / elapsed;
  console.info(`Performance Test Complete: ${detectionCount} detections in ${elapsed}s (${avgFps.toFixed(2)} FPS)`);
}, 30000);
```

## 🧪 Test Scenarios

### Scenario 1: Happy Expression
1. **Setup**: Smile widely, look at camera
2. **Expected**: Detect "happy" with >80% confidence
3. **Verify**: Green bounding box, happy emoji

### Scenario 2: Sad Expression
1. **Setup**: Frown, look down slightly
2. **Expected**: Detect "sad" with >70% confidence
3. **Verify**: Blue bounding box, sad emoji

### Scenario 3: Neutral Expression
1. **Setup**: Relaxed face, no expression
2. **Expected**: Detect "neutral" with >60% confidence
3. **Verify**: Gray bounding box, neutral emoji

### Scenario 4: Multiple Emotions
1. **Setup**: Change expressions every 5 seconds
2. **Expected**: Detection changes accordingly
3. **Verify**: Logs show emotion transitions

### Scenario 5: No Face
1. **Setup**: Move out of camera view
2. **Expected**: "No face detected" message
3. **Verify**: No bounding box, clear canvas

### Scenario 6: Poor Lighting
1. **Setup**: Dim lighting or backlighting
2. **Expected**: Lower confidence scores
3. **Verify**: Detection still works but with reduced accuracy

### Scenario 7: Congruent Chat
1. **Setup**: Smile + type "I'm happy"
2. **Expected**: Congruent emotion analysis
3. **Verify**: Green checkmark in bot response

### Scenario 8: Incongruent Chat
1. **Setup**: Sad face + type "I'm fine"
2. **Expected**: Incongruent emotion analysis
3. **Verify**: Warning icon in bot response

## 📝 Test Checklist

### Pre-Test Setup
- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] Camera available and not in use
- [ ] Good lighting conditions
- [ ] Browser developer tools open

### Model Loading Tests
- [ ] Models load without errors
- [ ] Progress bar shows 1/4 → 2/4 → 3/4 → 4/4
- [ ] "Ready to start webcam" message appears
- [ ] Start button becomes enabled

### Webcam Tests
- [ ] Camera permission granted
- [ ] Video preview appears
- [ ] Video is mirrored (text appears backwards)
- [ ] Canvas overlay positioned correctly

### Detection Tests
- [ ] Face detection works in good lighting
- [ ] Bounding box appears around face
- [ ] Emotion label shows above box
- [ ] Detection updates every ~500ms
- [ ] Multiple emotions detected correctly

### Chat Integration Tests
- [ ] Facial emotion badge appears on user messages
- [ ] Multimodal analysis card appears on bot responses
- [ ] Congruent emotions show green checkmark
- [ ] Incongruent emotions show warning icon
- [ ] Backend logs show emotion fusion messages

### Performance Tests
- [ ] Detection runs at ~2 FPS
- [ ] Memory usage < 100MB additional
- [ ] CPU usage < 20% additional
- [ ] No memory leaks after extended use

### Error Handling Tests
- [ ] Graceful handling of camera permission denial
- [ ] Proper error messages for network issues
- [ ] Recovery from temporary face detection failures
- [ ] Clean shutdown when webcam disabled

## 🎯 Success Criteria

### Functional Requirements
- ✅ Real-time facial emotion detection
- ✅ 7 emotions detected accurately
- ✅ Multimodal emotion fusion
- ✅ Incongruence detection
- ✅ User control (enable/disable)

### Performance Requirements
- ✅ Model load time < 5 seconds
- ✅ Detection frequency ~2 FPS
- ✅ Memory usage < 100MB
- ✅ CPU usage < 20%

### User Experience Requirements
- ✅ Intuitive UI controls
- ✅ Clear visual feedback
- ✅ Responsive design
- ✅ Error handling
- ✅ Privacy transparency

### Integration Requirements
- ✅ Seamless chat integration
- ✅ Backend API compatibility
- ✅ Cross-browser support
- ✅ Mobile responsiveness

## 🚨 Troubleshooting Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Models not loading | Check internet, refresh page |
| Camera not starting | Grant permission, close other apps |
| No face detected | Improve lighting, face camera |
| Black video preview | Check autoplay, CSS styling |
| Backend errors | Verify server running, check CORS |
| Low accuracy | Better lighting, clear expressions |
| Performance issues | Close other tabs, restart browser |
| Memory leaks | Disable/enable webcam, refresh page |

## 📞 Support

If tests fail or issues persist:

1. **Check Logs**: Browser console and backend terminal
2. **Verify Setup**: Ensure all dependencies installed
3. **Test Isolation**: Use HTML test page to isolate issues
4. **Documentation**: Review integration docs
5. **Community**: Check GitHub issues or create new one

---

**Happy Testing!** 🎭✨

The facial emotion detection feature should work seamlessly when all tests pass. Use this guide to verify functionality and debug any issues.