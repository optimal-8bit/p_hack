# Mental Health Chatbot - Full Stack Integration

This project integrates a React frontend with a FastAPI backend for a mental health support chatbot.

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

**Windows:**
```bash
start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

This will automatically:
- Start the backend server on port 8000
- Start the frontend dev server on port 5173
- Install dependencies if needed
- Open both in separate terminal windows

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd mental_health_chatbot/backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd react_web
npm run dev
```

## 📋 Prerequisites

### Backend Requirements
- Python 3.8+
- pip
- Virtual environment (recommended)

### Frontend Requirements
- Node.js 16+
- npm or yarn

## 🔧 Installation

### First Time Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Backend Setup**
   ```bash
   cd mental_health_chatbot/backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Download models (optional, for better responses)
   cd ..
   python scripts/download_models.py
   ```

3. **Frontend Setup**
   ```bash
   cd react_web
   
   # Install dependencies
   npm install
   
   # Create .env file (already created)
   # Verify it contains:
   # VITE_API_BASE_URL=http://localhost:8000
   # VITE_USE_MOCK=false
   ```

## 🌐 Access Points

Once both servers are running:

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Alternative Docs**: http://localhost:8000/redoc
- **Backend Health Check**: http://localhost:8000/api/health

## ✨ Features

### Integrated Features
- ✅ Real-time chat with streaming responses
- ✅ Emotion detection (7 emotions)
- ✅ Intent classification (6 categories)
- ✅ Crisis detection and safety responses
- ✅ Multilingual support (English, Hindi, French, Spanish)
- ✅ Session persistence across page reloads
- ✅ Backend health monitoring
- ✅ Model status display
- ✅ Conversation history

### Backend Features
- FastAPI REST API
- ONNX model inference
- SQLite database for history
- Context-aware responses
- Safety pattern detection
- Automatic language detection

### Frontend Features
- React 19 with Vite
- Redux for state management
- Animated background effects
- Video backgrounds during chat
- Responsive design
- Typewriter effect for responses
- Real-time health monitoring

## 🧪 Testing the Integration

### 1. Health Check
Open the frontend and check the sidebar. You should see:
- "HEALTHY" status
- All models showing as loaded (✓)

### 2. Basic Chat
Try these test messages:
- "Hello" - Should get a greeting
- "I'm feeling anxious" - Should detect anxiety intent
- "I'm happy today" - Should detect joy emotion

### 3. Crisis Detection
Try: "I want to hurt myself"
- Should receive crisis response
- Backend flags as crisis
- Provides helpline resources

### 4. Multilingual
Try messages in:
- Hindi: "मैं चिंतित महसूस कर रहा हूं"
- French: "Je me sens anxieux"
- Spanish: "Me siento ansioso"

Backend auto-detects language and responds accordingly.

## 🔍 Troubleshooting

### Backend Won't Start

**Error: "Module not found"**
```bash
cd mental_health_chatbot/backend
pip install -r requirements.txt
```

**Error: "Port 8000 already in use"**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Frontend Won't Start

**Error: "Cannot find module"**
```bash
cd react_web
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 5173 already in use"**
- Vite will automatically try the next available port
- Or kill the process using port 5173

### Backend Not Connecting

**Symptom**: "Backend Offline" in health status

**Solutions**:
1. Verify backend is running: http://localhost:8000
2. Check `.env` file has correct URL
3. Check browser console for CORS errors
4. Restart both servers

### Slow Responses

**Cause**: LLM generation is slow on CPU

**Solution**: In `backend/config.py`, ensure:
```python
LLM_ENABLED = False  # Use fast template responses
```

## 📁 Project Structure

```
.
├── mental_health_chatbot/
│   ├── backend/              # FastAPI backend
│   │   ├── api/             # API routes and schemas
│   │   ├── models/          # ML models
│   │   ├── pipeline/        # Processing pipeline
│   │   ├── response_engine/ # Response generation
│   │   ├── database/        # Database models
│   │   ├── config.py        # Configuration
│   │   └── main.py          # FastAPI app
│   └── frontend_test/       # Simple test UI (reference)
│
├── react_web/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── pages/          # Page components
│   │   └── styles/         # CSS styles
│   ├── .env                # Environment config
│   └── package.json
│
├── start-dev.bat           # Windows startup script
├── start-dev.sh            # Linux/Mac startup script
├── INTEGRATION_GUIDE.md    # Detailed integration docs
└── README_INTEGRATION.md   # This file
```

## 🔐 Environment Variables

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK=false
VITE_CHAT_STREAM_PATH=/api/chat
```

### Backend (config.py)
```python
HOST = "0.0.0.0"
PORT = 8000
LLM_ENABLED = False  # Fast template responses
DATABASE_URL = "sqlite+aiosqlite:///chat_history.db"
```

## 🚢 Production Deployment

### Backend
```bash
# Use production ASGI server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend
```bash
# Build for production
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting
```

### Environment Updates
- Update `VITE_API_BASE_URL` to production backend URL
- Update CORS settings in backend `main.py`
- Use environment variables for sensitive data

## 📚 Documentation

- **Integration Guide**: See `INTEGRATION_GUIDE.md` for detailed technical documentation
- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Backend README**: `mental_health_chatbot/README.md`
- **Frontend README**: `react_web/README.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📝 License

This project maintains the licenses of both the frontend and backend components.

## 🆘 Support

For issues:
1. Check the troubleshooting section above
2. Review `INTEGRATION_GUIDE.md` for detailed info
3. Check backend logs in terminal
4. Check browser console for frontend errors
5. Test with simple UI: `mental_health_chatbot/frontend_test/index.html`

## 🎯 Next Steps

After successful integration, consider:
1. Loading chat history from backend
2. Adding language selector UI
3. Implementing emotion visualization
4. Adding voice input support
5. Creating offline mode with service workers
6. Adding conversation export feature

---

**Happy Coding! 🚀**
