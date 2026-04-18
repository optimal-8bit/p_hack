# Frontend-Backend Integration Guide

## Overview

This guide explains how the React frontend (`react_web`) has been integrated with the Mental Health Chatbot backend (`mental_health_chatbot/backend`).

## Architecture

### Backend (FastAPI)
- **Location**: `mental_health_chatbot/backend/`
- **Port**: 8000
- **Base URL**: `http://localhost:8000`
- **API Prefix**: `/api`

### Frontend (React + Vite)
- **Location**: `react_web/`
- **Dev Port**: 5173 (default Vite)
- **Build Output**: `react_web/dist/`

## Integration Changes

### 1. Environment Configuration

Created `.env` file in `react_web/`:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK=false
VITE_CHAT_STREAM_PATH=/api/chat
```

### 2. Chat Service Update

**File**: `react_web/src/services/chatService.js`

**Key Changes**:
- Removed dependency on generic `apiClient` for chat
- Added direct integration with Mental Health Chatbot API
- Implemented session management using `sessionStorage`
- Added streaming simulation for typewriter effect
- Integrated backend response metadata (emotion, intent, language, crisis detection)

**New Methods**:
- `streamReply()` - Main chat method with streaming simulation
- `getHistory()` - Fetch conversation history
- `clearSession()` - Clear session and reset
- `getHealth()` - Check backend health status
- `getSupportedLanguages()` - Get available languages

### 3. Health Status Component

**Files**:
- `react_web/src/components/chat/HealthStatus.jsx`
- `react_web/src/components/chat/HealthStatus.css`

**Features**:
- Real-time backend health monitoring
- Model loading status display
- Auto-refresh every 30 seconds
- Manual refresh button
- Error handling with retry

### 4. Sidebar Integration

**File**: `react_web/src/components/chat/Sidebar.jsx`

**Changes**:
- Added `HealthStatus` component
- Displays backend status at the top of sidebar
- Shows all loaded models and their status

## API Endpoints Used

### 1. Chat Endpoint
```
POST /api/chat
```

**Request**:
```json
{
  "session_id": "session-1234567890-abc",
  "message": "I'm feeling anxious"
}
```

**Response**:
```json
{
  "response_text": "I hear you. Anxiety can be really challenging...",
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

### 2. Health Check
```
GET /api/health
```

**Response**:
```json
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

### 3. Session History
```
GET /api/session/{session_id}/history
```

**Response**:
```json
{
  "session_id": "session-1234567890-abc",
  "turns": [
    {
      "user_message": "I'm feeling anxious",
      "bot_response": "I hear you...",
      "emotion": "fear",
      "intent": "anxiety and panic",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "total_turns": 1
}
```

### 4. Clear Session
```
DELETE /api/session/{session_id}
```

**Response**:
```json
{
  "status": "cleared",
  "session_id": "session-1234567890-abc"
}
```

### 5. Supported Languages
```
GET /api/supported-languages
```

**Response**:
```json
{
  "languages": [
    { "code": "en", "name": "English" },
    { "code": "hi", "name": "Hindi" },
    { "code": "fr", "name": "French" },
    { "code": "es", "name": "Spanish" }
  ]
}
```

## Session Management

### Session ID Generation
- Generated on first chat interaction
- Stored in `sessionStorage` for persistence across page reloads
- Format: `session-{timestamp}-{random}`
- Cleared when user explicitly clears session

### Session Persistence
- Session ID persists across page reloads
- Conversation context maintained on backend
- Can be cleared via UI or programmatically

## Features Integrated

### ✅ Real-time Chat
- Typewriter effect for bot responses
- Streaming simulation (20ms per character)
- Error handling and retry logic
- Session-based conversation context

### ✅ Backend Health Monitoring
- Live status indicator
- Model loading status
- Auto-refresh every 30 seconds
- Manual refresh option

### ✅ Emotion & Intent Detection
- Displayed in response metadata
- Confidence scores included
- All 7 emotions supported (anger, disgust, fear, joy, neutral, sadness, surprise)
- 6 intent categories

### ✅ Crisis Detection
- Automatic crisis pattern detection
- Special crisis response handling
- Backend flags crisis messages

### ✅ Multilingual Support
- English, Hindi, French, Spanish
- Automatic language detection
- Translation handled by backend

### ✅ Mock Mode
- Set `VITE_USE_MOCK=true` to use mock responses
- Useful for frontend development without backend
- Simulates realistic delays and streaming

## Running the Application

### 1. Start Backend

```bash
cd mental_health_chatbot/backend

# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the server
python main.py
```

Backend will start at: `http://localhost:8000`

### 2. Start Frontend

```bash
cd react_web

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend will start at: `http://localhost:5173`

### 3. Access the Application

Open your browser and navigate to:
- Frontend: `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/docs`
- Backend Health: `http://localhost:8000/api/health`

## Testing the Integration

### 1. Check Backend Health
- Open the frontend
- Look at the sidebar "Backend Status" section
- Should show "HEALTHY" with all models loaded

### 2. Send a Test Message
- Type: "I'm feeling anxious"
- Should receive empathetic response
- Check metadata shows emotion and intent

### 3. Test Crisis Detection
- Type: "I want to hurt myself"
- Should receive crisis response with resources
- Backend flags `is_crisis: true`

### 4. Test Multilingual
- Type in Hindi, French, or Spanish
- Backend auto-detects language
- Response in same language

### 5. Test Session Persistence
- Send a few messages
- Refresh the page
- Session should persist (same session ID)

## Troubleshooting

### Backend Not Connecting

**Symptom**: "Backend Offline" in health status

**Solutions**:
1. Check backend is running: `http://localhost:8000`
2. Check CORS is enabled (already configured)
3. Verify `.env` has correct `VITE_API_BASE_URL`
4. Check browser console for errors

### Models Not Loading

**Symptom**: Health shows models as "not loaded"

**Solutions**:
1. Run model download script:
   ```bash
   cd mental_health_chatbot
   python scripts/download_models.py
   ```
2. Check `backend/onnx_models/` directory exists
3. Verify models are in correct subdirectories

### Slow Responses

**Symptom**: Long wait times for responses

**Causes**:
- LLM generation enabled (slow on CPU)
- First request (model warmup)
- Large context window

**Solutions**:
1. Keep `LLM_ENABLED = False` in `backend/config.py` for fast template responses
2. Use GPU if available
3. Reduce `CONTEXT_WINDOW_SIZE` in config

### Session Not Persisting

**Symptom**: Session resets on page reload

**Solutions**:
1. Check browser allows `sessionStorage`
2. Not in incognito/private mode
3. Check browser console for errors

## Development Tips

### Mock Mode for Frontend Development

When working on frontend without backend:

```env
VITE_USE_MOCK=true
```

This uses the mock responses from `src/mock/mockResponses.js`.

### Hot Reload

Both frontend and backend support hot reload:
- **Frontend**: Vite automatically reloads on file changes
- **Backend**: Use `uvicorn` with `--reload` flag (already configured in `main.py`)

### API Testing

Use the interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Browser DevTools

Monitor network requests:
1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "Fetch/XHR"
4. Watch API calls in real-time

## Production Deployment

### Backend Deployment

1. Set environment variables:
   ```bash
   export HOST=0.0.0.0
   export PORT=8000
   ```

2. Use production ASGI server:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

### Frontend Deployment

1. Update `.env` for production:
   ```env
   VITE_API_BASE_URL=https://your-backend-domain.com
   VITE_USE_MOCK=false
   ```

2. Build for production:
   ```bash
   npm run build
   ```

3. Deploy `dist/` folder to:
   - Vercel
   - Netlify
   - AWS S3 + CloudFront
   - Any static hosting

### CORS Configuration

For production, update backend CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## File Structure

```
.
├── mental_health_chatbot/
│   ├── backend/
│   │   ├── api/
│   │   │   ├── routes.py          # API endpoints
│   │   │   └── schemas.py         # Request/response models
│   │   ├── config.py              # Configuration
│   │   ├── main.py                # FastAPI app
│   │   └── ...
│   └── frontend_test/             # Simple test UI (reference)
│       ├── index.html
│       └── app.js
│
├── react_web/
│   ├── src/
│   │   ├── components/
│   │   │   └── chat/
│   │   │       ├── HealthStatus.jsx      # NEW: Health monitoring
│   │   │       ├── HealthStatus.css
│   │   │       └── Sidebar.jsx           # UPDATED: Added health status
│   │   ├── services/
│   │   │   └── chatService.js            # UPDATED: Backend integration
│   │   ├── pages/
│   │   │   └── MentalHealthChatPage.jsx  # Main chat page
│   │   └── ...
│   ├── .env                               # NEW: Environment config
│   ├── .env.example                       # NEW: Example config
│   └── package.json
│
└── INTEGRATION_GUIDE.md                   # This file
```

## Next Steps

### Potential Enhancements

1. **Chat History Loading**
   - Load previous conversations from backend
   - Display in sidebar
   - Resume conversations

2. **Language Selector**
   - UI to select preferred language
   - Use `/api/supported-languages` endpoint
   - Force specific language for responses

3. **Emotion Visualization**
   - Display emotion confidence scores
   - Show emotion trends over conversation
   - Visual indicators for emotional state

4. **Crisis Resources**
   - Display crisis hotlines when detected
   - Location-based resources
   - Emergency contact integration

5. **Export Conversation**
   - Download chat history
   - PDF or text format
   - Privacy-preserving export

6. **Voice Input**
   - Speech-to-text integration
   - Multilingual voice support
   - Accessibility feature

7. **Offline Mode**
   - Service worker for offline access
   - Cache responses
   - Queue messages when offline

## Support

For issues or questions:
1. Check backend logs: `mental_health_chatbot/backend/`
2. Check browser console for frontend errors
3. Review API docs: `http://localhost:8000/docs`
4. Test with simple UI: `mental_health_chatbot/frontend_test/index.html`

## License

This integration maintains the licenses of both projects.
