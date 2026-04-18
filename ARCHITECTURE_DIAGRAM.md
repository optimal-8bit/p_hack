# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:5173                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REACT FRONTEND                              │
│                      (react_web/)                                │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Pages                                                    │   │
│  │  └─ MentalHealthChatPage.jsx                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Components                                               │   │
│  │  ├─ ChatContainer                                        │   │
│  │  ├─ MessageBubble                                        │   │
│  │  ├─ ChatInput                                            │   │
│  │  ├─ Sidebar                                              │   │
│  │  └─ HealthStatus ⭐ NEW                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Services                                                 │   │
│  │  └─ chatService.js ⭐ UPDATED                            │   │
│  │     ├─ streamReply()                                     │   │
│  │     ├─ getHealth()                                       │   │
│  │     ├─ getHistory()                                      │   │
│  │     ├─ clearSession()                                    │   │
│  │     └─ getSupportedLanguages()                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  State Management                                         │   │
│  │  ├─ sessionStorage (session_id)                          │   │
│  │  └─ React State (messages, typing, etc.)                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              │ http://localhost:8000
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│              (mental_health_chatbot/backend/)                    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  API Routes (api/routes.py)                              │   │
│  │  ├─ POST   /api/chat                                     │   │
│  │  ├─ GET    /api/health                                   │   │
│  │  ├─ GET    /api/session/{id}/history                     │   │
│  │  ├─ DELETE /api/session/{id}                             │   │
│  │  └─ GET    /api/supported-languages                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Pipeline (pipeline/)                                     │   │
│  │  ├─ Orchestrator                                         │   │
│  │  ├─ Preprocessor                                         │   │
│  │  ├─ Context Tracker                                      │   │
│  │  ├─ Safety Checker                                       │   │
│  │  └─ Message Type Detector                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Models (models/)                                         │   │
│  │  ├─ Emotion Classifier (ONNX)                           │   │
│  │  ├─ Intent Classifier (ONNX)                            │   │
│  │  └─ Translator (Transformers)                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Response Engine (response_engine/)                       │   │
│  │  ├─ Template Selector                                    │   │
│  │  ├─ Response Builder                                     │   │
│  │  ├─ Gemini Generator (optional)                          │   │
│  │  └─ LLM Generator (optional)                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Database (database/)                                     │   │
│  │  └─ SQLite (chat_history.db)                            │   │
│  │     ├─ chat_turns                                        │   │
│  │     └─ crisis_events                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### Chat Message Flow

```
User Types Message
       │
       ▼
┌──────────────────┐
│  ChatInput       │
│  Component       │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  handleSendMsg   │
│  (Page State)    │
└──────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  chatService.streamReply()           │
│  ├─ Get session_id from storage      │
│  ├─ Build request payload            │
│  └─ POST /api/chat                   │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Backend: /api/chat                  │
│  ├─ Validate request                 │
│  ├─ Get/create session               │
│  └─ Call orchestrator                │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Orchestrator.process_message()      │
│  ├─ Preprocess text                  │
│  ├─ Detect language                  │
│  ├─ Translate to English (if needed) │
│  ├─ Check safety/crisis              │
│  ├─ Classify emotion                 │
│  ├─ Classify intent                  │
│  ├─ Get context                      │
│  ├─ Generate response                │
│  ├─ Translate back (if needed)       │
│  └─ Update context                   │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Backend: Return Response            │
│  {                                    │
│    response_text: "...",             │
│    emotion: {...},                   │
│    intent: {...},                    │
│    is_crisis: false,                 │
│    detected_language: "en",          │
│    ...                               │
│  }                                   │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Frontend: Simulate Streaming        │
│  ├─ Split response into characters   │
│  ├─ Yield char every 20ms            │
│  └─ Update message state             │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  MessageBubble Component             │
│  └─ Display with typewriter effect   │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Save to Database (async)            │
│  ├─ chat_turns table                 │
│  └─ crisis_events (if crisis)        │
└──────────────────────────────────────┘
```

### Health Check Flow

```
Component Mount / Timer
       │
       ▼
┌──────────────────────────────────────┐
│  HealthStatus Component              │
│  └─ useEffect() / setInterval()      │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  chatService.getHealth()             │
│  └─ GET /api/health                  │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Backend: /api/health                │
│  ├─ Check emotion model              │
│  ├─ Check intent model               │
│  ├─ Check translators                │
│  └─ Determine status                 │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Return Health Status                │
│  {                                    │
│    status: "healthy",                │
│    models_loaded: {                  │
│      emotion_classifier: true,       │
│      intent_classifier: true,        │
│      translator_hi: true,            │
│      ...                             │
│    },                                │
│    version: "1.0.0"                  │
│  }                                   │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  HealthStatus Component              │
│  ├─ Update state                     │
│  ├─ Display status indicator         │
│  └─ Show model statuses              │
└──────────────────────────────────────┘
```

## Data Flow

### Session Management

```
┌─────────────────────────────────────────────────────────┐
│  Browser sessionStorage                                  │
│  ├─ Key: "mental_health_session_id"                     │
│  └─ Value: "session-1234567890-abc"                     │
└─────────────────────────────────────────────────────────┘
                    │
                    │ Sent with every request
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Backend Context Tracker                                 │
│  ├─ In-memory session contexts                          │
│  ├─ Conversation history (last 5 turns)                 │
│  └─ Emotion/intent trends                               │
└─────────────────────────────────────────────────────────┘
                    │
                    │ Persisted
                    ▼
┌─────────────────────────────────────────────────────────┐
│  SQLite Database                                         │
│  ├─ chat_turns table                                    │
│  │  ├─ session_id                                       │
│  │  ├─ user_message                                     │
│  │  ├─ bot_response                                     │
│  │  ├─ emotion                                          │
│  │  ├─ intent                                           │
│  │  └─ timestamp                                        │
│  └─ crisis_events table                                 │
│     ├─ session_id                                       │
│     ├─ crisis_type                                      │
│     └─ timestamp                                        │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
```
┌─────────────────────────────────────┐
│  React 19                            │
│  ├─ Vite (build tool)               │
│  ├─ Redux Toolkit (state)           │
│  ├─ React Router (routing)          │
│  ├─ GSAP (animations)               │
│  └─ Lucide React (icons)            │
└─────────────────────────────────────┘
```

### Backend
```
┌─────────────────────────────────────┐
│  FastAPI                             │
│  ├─ Uvicorn (ASGI server)           │
│  ├─ Pydantic (validation)           │
│  ├─ SQLAlchemy (ORM)                │
│  ├─ ONNX Runtime (inference)        │
│  ├─ Transformers (translation)      │
│  └─ SQLite (database)               │
└─────────────────────────────────────┘
```

## Network Communication

### API Endpoints

```
┌──────────────────────────────────────────────────────────────┐
│  POST /api/chat                                               │
│  ├─ Request:  { session_id, message }                        │
│  └─ Response: { response_text, emotion, intent, ... }        │
├──────────────────────────────────────────────────────────────┤
│  GET /api/health                                              │
│  ├─ Request:  None                                            │
│  └─ Response: { status, models_loaded, version }             │
├──────────────────────────────────────────────────────────────┤
│  GET /api/session/{session_id}/history                        │
│  ├─ Request:  None                                            │
│  └─ Response: { session_id, turns[], total_turns }           │
├──────────────────────────────────────────────────────────────┤
│  DELETE /api/session/{session_id}                             │
│  ├─ Request:  None                                            │
│  └─ Response: { status, session_id }                         │
├──────────────────────────────────────────────────────────────┤
│  GET /api/supported-languages                                 │
│  ├─ Request:  None                                            │
│  └─ Response: { languages: [{ code, name }] }                │
└──────────────────────────────────────────────────────────────┘
```

### CORS Configuration

```
┌─────────────────────────────────────┐
│  Backend CORS Middleware             │
│  ├─ allow_origins: ["*"]            │
│  ├─ allow_credentials: true         │
│  ├─ allow_methods: ["*"]            │
│  └─ allow_headers: ["*"]            │
└─────────────────────────────────────┘
         │
         │ Allows requests from
         ▼
┌─────────────────────────────────────┐
│  Frontend (any origin)               │
│  └─ http://localhost:5173           │
└─────────────────────────────────────┘
```

## Deployment Architecture

### Development
```
┌──────────────────┐     ┌──────────────────┐
│  Frontend Dev    │     │  Backend Dev     │
│  Vite Server     │────▶│  Uvicorn         │
│  :5173           │     │  :8000           │
└──────────────────┘     └──────────────────┘
```

### Production
```
┌──────────────────┐     ┌──────────────────┐
│  Static Hosting  │     │  ASGI Server     │
│  (Vercel/        │────▶│  (Gunicorn +     │
│   Netlify)       │     │   Uvicorn)       │
└──────────────────┘     └──────────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────────────────────────┐
│  Security Layers                                         │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Input Validation (Pydantic)                   │    │
│  │  ├─ Max message length: 1000 chars             │    │
│  │  └─ Session ID format validation               │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Safety Checks                                  │    │
│  │  ├─ Crisis pattern detection                   │    │
│  │  ├─ Harmful content filtering                  │    │
│  │  └─ Rate limiting (future)                     │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Privacy                                        │    │
│  │  ├─ No external API calls                      │    │
│  │  ├─ Local model inference                      │    │
│  │  └─ Session-based (no user accounts)           │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Scalable design
- ✅ Privacy-first approach
- ✅ Real-time responsiveness
- ✅ Offline-capable backend
- ✅ Easy to maintain and extend
