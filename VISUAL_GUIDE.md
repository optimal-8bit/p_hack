# Visual Guide - What You Should See

This guide shows what the integrated application should look like when running correctly.

## 1. Starting the Application

### Backend Terminal
```
==========================================
Starting Mental Health Chatbot Backend
==========================================
Creating database tables...
Loading emotion classifier...
✓ Emotion classifier loaded (ONNX)
Loading intent classifier...
✓ Intent classifier loaded (ONNX)
Initializing translation manager...
✓ Translation manager initialized (models will be lazy-loaded)
Initializing chat orchestrator...
✓ Chat orchestrator initialized
==========================================
Backend startup complete!
Server running at http://0.0.0.0:8000
API docs available at http://localhost:8000/docs
==========================================
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Frontend Terminal
```
  VITE v8.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

## 2. Frontend UI Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Mental Health Support Chat                        │
├──────────────┬──────────────────────────────────────────────────────┤
│              │                                                       │
│  SIDEBAR     │              MAIN CHAT AREA                          │
│              │                                                       │
│ ┌──────────┐│                                                       │
│ │ + New    ││              ┌─────────────────────┐                 │
│ │   Chat   ││              │  Mental Health      │                 │
│ └──────────┘│              │  Support            │                 │
│              │              │                     │                 │
│ Backend      │              │  I'm here to listen │                 │
│ Status       │              │  and support you.   │                 │
│ ┌──────────┐│              │  How are you        │                 │
│ │ ● HEALTHY││              │  feeling today?     │                 │
│ │ v1.0.0   ││              └─────────────────────┘                 │
│ │          ││                                                       │
│ │ Models:  ││                                                       │
│ │ emotion  ✓│                                                       │
│ │ intent   ✓│                                                       │
│ │ trans_hi ✓│                                                       │
│ │ trans_fr ✓│                                                       │
│ │ trans_es ✓│                                                       │
│ │          ││                                                       │
│ │ [Refresh]││                                                       │
│ └──────────┘│                                                       │
│              │                                                       │
│ Recents      │                                                       │
│ ▼            │                                                       │
│ (empty)      │                                                       │
│              │                                                       │
│              │                                                       │
│              │                                                       │
│              │  ┌─────────────────────────────────────────────┐   │
│              │  │ Type your message here...            [Send] │   │
│              │  └─────────────────────────────────────────────┘   │
└──────────────┴──────────────────────────────────────────────────────┘
```

## 3. Health Status Display

### Healthy Status
```
┌─────────────────────┐
│ Backend Status      │
├─────────────────────┤
│ ● HEALTHY           │
│ v1.0.0              │
├─────────────────────┤
│ emotion_classifier ✓│
│ intent_classifier  ✓│
│ translator_hi      ✓│
│ translator_fr      ✓│
│ translator_es      ✓│
├─────────────────────┤
│    [Refresh]        │
└─────────────────────┘
```

### Offline Status
```
┌─────────────────────┐
│ Backend Status      │
├─────────────────────┤
│ ● Backend Offline   │
│ Cannot connect to   │
│ server              │
├─────────────────────┤
│    [Retry]          │
└─────────────────────┘
```

## 4. Chat Conversation Example

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                                                              │
│  Hello! I'm here to listen and support you.                 │
│  How are you feeling today?                                 │
│                                                              │
│                                                              │
│                                      I'm feeling anxious ■  │
│                                                              │
│                                                              │
│  I hear you. Anxiety can be really challenging. Try taking  │
│  a few deep breaths. What's on your mind?                   │
│                                                              │
│  [emotion: fear 85%] [intent: anxiety and panic]            │
│  [lang: en] [245ms]                                          │
│                                                              │
│                                                              │
│                          I have a big presentation today ■  │
│                                                              │
│                                                              │
│  Presentations can definitely trigger anxiety. Remember,    │
│  it's normal to feel nervous. Have you prepared well?       │
│                                                              │
│  [emotion: fear 78%] [intent: stress and overwhelm]         │
│  [lang: en] [198ms]                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 5. Message Types

### User Message (Right-aligned, Dark Background)
```
                                    Hello, how are you? ■
```

### Bot Message (Left-aligned, Transparent Background)
```
I'm doing well, thanks for asking. How are you feeling?

[emotion: neutral 92%] [intent: general emotional support]
[lang: en] [156ms]
```

### Crisis Message (Red Border)
```
┌─────────────────────────────────────────────────────────┐
│ 🆘 Crisis Response                                       │
│                                                          │
│ I'm really concerned about you. Please reach out to a   │
│ crisis helpline immediately:                            │
│                                                          │
│ National Suicide Prevention Lifeline: 988               │
│ or 1-800-273-8255                                       │
│                                                          │
│ You matter, and help is available.                      │
└─────────────────────────────────────────────────────────┘
```

### Typing Indicator
```
● ● ●  (animated bouncing dots)
```

## 6. Browser Console (DevTools)

### Successful Request
```
[Network Tab]
POST /api/chat
Status: 200 OK
Time: 245ms

Request:
{
  "session_id": "session-1234567890-abc",
  "message": "I'm feeling anxious"
}

Response:
{
  "response_text": "I hear you. Anxiety can be...",
  "detected_language": "en",
  "emotion": {
    "emotion": "fear",
    "confidence": 0.85,
    "all_scores": {}
  },
  "intent": {
    "intent": "anxiety and panic",
    "confidence": 0.92
  },
  "turn_number": 1,
  "is_crisis": false,
  "processing_time_ms": 245.3,
  "session_id": "session-1234567890-abc"
}
```

### Health Check
```
[Network Tab]
GET /api/health
Status: 200 OK
Time: 12ms

Response:
{
  "status": "healthy",
  "models_loaded": {
    "emotion_classifier": true,
    "intent_classifier": true,
    "translator_hi": true,
    "translator_fr": true,
    "translator_es": true
  },
  "version": "1.0.0"
}
```

## 7. Session Storage (DevTools > Application)

```
Key: mental_health_session_id
Value: session-1705320000000-abc123def
```

## 8. Backend API Documentation

### Swagger UI (http://localhost:8000/docs)
```
┌─────────────────────────────────────────────────────────┐
│  Mental Health Chatbot API                               │
│  Version: 1.0.0                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  POST /api/chat                                          │
│  ▼ Send a message to the chatbot                        │
│                                                          │
│  GET /api/health                                         │
│  ▼ Check system health and model status                 │
│                                                          │
│  GET /api/session/{session_id}/history                   │
│  ▼ Get conversation history                             │
│                                                          │
│  DELETE /api/session/{session_id}                        │
│  ▼ Clear session context                                │
│                                                          │
│  GET /api/supported-languages                            │
│  ▼ List supported languages                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 9. Mobile View

```
┌─────────────────────┐
│ ☰  Mental Health    │
├─────────────────────┤
│                     │
│  Mental Health      │
│  Support            │
│                     │
│  I'm here to listen │
│  and support you.   │
│  How are you        │
│  feeling today?     │
│                     │
│                     │
│                     │
│                     │
│                     │
│                     │
│                     │
│                     │
│                     │
├─────────────────────┤
│ Type message... [>] │
└─────────────────────┘
```

## 10. Error States

### Backend Connection Error
```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│  Sorry, I encountered an error. Please try again.       │
│                                                          │
│  [Error: Cannot connect to backend server]              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Empty Message Validation
```
┌─────────────────────────────────────────────────────────┐
│ [Type your message here...]                      [Send] │
└─────────────────────────────────────────────────────────┘
                                                    ↑
                                              (disabled)
```

## 11. Animations

### Typewriter Effect
```
Frame 1: "I"
Frame 2: "I h"
Frame 3: "I hea"
Frame 4: "I hear "
Frame 5: "I hear you"
Frame 6: "I hear you."
...
(20ms between each character)
```

### Loading Indicator
```
Frame 1: ●○○
Frame 2: ○●○
Frame 3: ○○●
Frame 4: ○●○
(repeating)
```

### Background Animation
```
- Light rays emanating from top center
- Subtle movement following mouse
- Smooth transitions
- Video background during chat (optional)
```

## 12. Multilingual Examples

### Hindi
```
User: मैं चिंतित महसूस कर रहा हूं

Bot: मैं आपकी बात सुन रहा हूं। चिंता वास्तव में चुनौतीपूर्ण हो सकती है...

[emotion: fear 82%] [intent: anxiety and panic]
[lang: hi] [312ms]
```

### French
```
User: Je me sens anxieux

Bot: Je vous entends. L'anxiété peut être vraiment difficile...

[emotion: fear 85%] [intent: anxiety and panic]
[lang: fr] [298ms]
```

### Spanish
```
User: Me siento ansioso

Bot: Te escucho. La ansiedad puede ser realmente desafiante...

[emotion: fear 87%] [intent: anxiety and panic]
[lang: es] [285ms]
```

## 13. Performance Indicators

### Good Performance
```
Processing Time: 150-300ms
Health Status: ● HEALTHY
All Models: ✓ Loaded
Response: Smooth typewriter effect
No lag in UI
```

### Degraded Performance
```
Processing Time: 500-1000ms
Health Status: ● DEGRADED
Some Models: ✗ Not loaded
Response: Slower but functional
Possible UI lag
```

## 14. Database Entries

### Chat Turns Table
```
| id | session_id          | user_message      | bot_response     | emotion | intent           | timestamp           |
|----|---------------------|-------------------|------------------|---------|------------------|---------------------|
| 1  | session-123-abc     | I'm feeling sad   | I'm sorry you... | sadness | sadness and...   | 2024-01-15 10:30:00 |
| 2  | session-123-abc     | I feel lonely     | Loneliness can...| sadness | loneliness and...| 2024-01-15 10:31:00 |
```

### Crisis Events Table
```
| id | session_id          | crisis_type      | timestamp           |
|----|---------------------|------------------|---------------------|
| 1  | session-456-def     | crisis_detected  | 2024-01-15 11:00:00 |
```

---

## What Success Looks Like

✅ **Backend Terminal**: Shows "Backend startup complete!" with all models loaded

✅ **Frontend Browser**: Loads without errors, shows health status as "HEALTHY"

✅ **Chat Interface**: Messages send and receive smoothly with typewriter effect

✅ **Health Status**: Green indicator, all models showing checkmarks

✅ **Session Persistence**: Session ID stays same after page reload

✅ **Emotion/Intent**: Metadata displays correctly under bot messages

✅ **Multilingual**: Non-English messages get responses in same language

✅ **Crisis Detection**: Crisis messages trigger appropriate responses

✅ **Performance**: Response times under 500ms, smooth animations

✅ **No Errors**: Clean console logs, no red errors in browser or terminal

---

## Troubleshooting Visual Cues

### ❌ Backend Not Running
- Health status shows red dot
- "Backend Offline" message
- Cannot send messages

### ❌ Models Not Loaded
- Health status shows some ✗ marks
- Status may show "DEGRADED"
- Responses may be less accurate

### ❌ Network Error
- Error message in chat
- Red text in console
- Failed network requests in DevTools

### ❌ Session Issues
- Session ID changes on reload
- Context not maintained
- History not loading

---

Use this visual guide to verify your integration is working correctly!
