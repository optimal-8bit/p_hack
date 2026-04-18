# 🚀 START HERE - Quick Integration Guide

Welcome! This document will get you up and running in 5 minutes.

## 📋 What Was Integrated?

The **React frontend** (`react_web/`) is now fully integrated with the **Mental Health Chatbot backend** (`mental_health_chatbot/backend/`).

### What Works Now:
✅ Real-time chat with emotion & intent detection  
✅ Crisis detection and safety responses  
✅ Multilingual support (English, Hindi, French, Spanish)  
✅ Session persistence across page reloads  
✅ Backend health monitoring in UI  
✅ Typewriter effect for responses  

## 🎯 Quick Start (Choose One)

### Option 1: Automated (Easiest) ⭐

**Windows:**
```bash
start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

This automatically starts both servers and installs dependencies if needed.

### Option 2: Manual

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

## 🌐 Access the Application

Once both servers are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✅ Verify It's Working

1. Open http://localhost:5173
2. Check sidebar shows "HEALTHY" status with green dot
3. Type "Hello" and send
4. You should get a response with typewriter effect
5. Check metadata shows emotion and intent

## 🧪 Test Features

### Basic Chat
```
You: Hello
Bot: Hello! I'm here to support you. How are you feeling?
```

### Emotion Detection
```
You: I'm feeling sad
Bot: [Response with emotion: sadness detected]
```

### Crisis Detection
```
You: I want to hurt myself
Bot: [Crisis response with helpline resources]
```

### Multilingual
```
You: मैं चिंतित हूं (Hindi)
Bot: [Response in Hindi]
```

## 📚 Documentation

Choose based on what you need:

### For Quick Start
- **This file** - You're reading it! ✓
- `README_INTEGRATION.md` - Quick start guide
- `VISUAL_GUIDE.md` - What you should see

### For Understanding
- `INTEGRATION_COMPLETE.md` - What was done
- `ARCHITECTURE_DIAGRAM.md` - How it works
- `INTEGRATION_GUIDE.md` - Technical details

### For Testing
- `INTEGRATION_CHECKLIST.md` - Verification checklist

## 🔧 First Time Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm

### Backend Setup (First Time Only)
```bash
cd mental_health_chatbot/backend

# Create virtual environment (optional)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download models (IMPORTANT for emotion & intent detection)
cd ..
python scripts/download_models.py
```

**📥 Model Installation**: See `INSTALL_MODELS.md` for detailed instructions on installing emotion and intent models.

### Frontend Setup (First Time Only)
```bash
cd react_web

# Install dependencies
npm install

# Verify .env file exists and contains:
# VITE_API_BASE_URL=http://localhost:8000
# VITE_USE_MOCK=false
```

## 🐛 Common Issues

### Backend Won't Start
```bash
cd mental_health_chatbot/backend
pip install -r requirements.txt
```

### Frontend Won't Start
```bash
cd react_web
npm install
```

### "Backend Offline" in UI
1. Check backend is running: http://localhost:8000
2. Check `.env` has correct URL
3. Restart both servers

### Slow Responses
In `mental_health_chatbot/backend/config.py`, ensure:
```python
LLM_ENABLED = False  # Fast template responses
```

### Port Already in Use
**Backend (8000):**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

**Frontend (5173):**
- Vite will automatically use next available port

## 📁 Project Structure

```
.
├── mental_health_chatbot/
│   └── backend/              # FastAPI backend (port 8000)
│       ├── api/             # API routes
│       ├── models/          # ML models
│       ├── pipeline/        # Processing pipeline
│       └── main.py          # Start here
│
├── react_web/               # React frontend (port 5173)
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── services/       # API integration ⭐
│   │   └── pages/          # Page components
│   └── .env                # Configuration ⭐
│
├── start-dev.bat           # Windows startup ⭐
├── start-dev.sh            # Linux/Mac startup ⭐
└── START_HERE.md           # This file
```

## 🎨 What You'll See

### Sidebar (Left)
- Backend health status
- Model loading status
- New chat button
- Chat history (future)

### Main Area (Center)
- Welcome message
- Chat messages
- User messages (right, dark)
- Bot messages (left, with metadata)
- Input box at bottom

### Metadata (Under Bot Messages)
```
[emotion: fear 85%] [intent: anxiety and panic] [lang: en] [245ms]
```

## 🔐 Features

### Session Management
- Session ID stored in browser
- Persists across page reloads
- Can be cleared via UI

### Emotion Detection
7 emotions: anger, disgust, fear, joy, neutral, sadness, surprise

### Intent Classification
6 intents: anxiety, depression, stress, loneliness, anger, general support

### Crisis Detection
Automatic detection with helpline resources

### Multilingual
English, Hindi, French, Spanish with auto-detection

## 🚢 Production Deployment

### Backend
```bash
# Update CORS in main.py for your domain
# Use production ASGI server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend
```bash
# Update .env
VITE_API_BASE_URL=https://your-backend-domain.com

# Build
npm run build

# Deploy dist/ folder to Vercel/Netlify/etc
```

## 📞 Need Help?

1. Check `INTEGRATION_CHECKLIST.md` for verification steps
2. Review `VISUAL_GUIDE.md` to see what's expected
3. Read `INTEGRATION_GUIDE.md` for technical details
4. Check browser console for errors
5. Check backend terminal for logs

## 🎯 Next Steps

After verifying everything works:

1. **Customize Responses**
   - Edit `backend/response_engine/templates.py`
   - Add more response templates

2. **Add Features**
   - Chat history loading
   - Language selector UI
   - Emotion visualization
   - Voice input

3. **Deploy**
   - Follow production deployment guide
   - Update environment variables
   - Configure CORS

4. **Monitor**
   - Use health endpoint
   - Check logs
   - Monitor performance

## 🎉 Success Checklist

- [ ] Both servers start without errors
- [ ] Frontend loads at http://localhost:5173
- [ ] Health status shows "HEALTHY"
- [ ] Can send and receive messages
- [ ] Typewriter effect works
- [ ] Emotion/intent detected
- [ ] Session persists on reload
- [ ] No console errors

## 📝 Quick Commands Reference

```bash
# Start everything (automated)
start-dev.bat              # Windows
./start-dev.sh             # Linux/Mac

# Start backend only
cd mental_health_chatbot/backend
python main.py

# Start frontend only
cd react_web
npm run dev

# Install backend dependencies
cd mental_health_chatbot/backend
pip install -r requirements.txt

# Install frontend dependencies
cd react_web
npm install

# Download models
cd mental_health_chatbot
python scripts/download_models.py

# Build frontend for production
cd react_web
npm run build

# Check backend health
curl http://localhost:8000/api/health

# View API docs
# Open: http://localhost:8000/docs
```

## 🌟 Key Files Modified

### New Files
- `react_web/.env` - Configuration
- `react_web/src/components/chat/HealthStatus.jsx` - Health monitoring
- `start-dev.bat` / `start-dev.sh` - Startup scripts

### Modified Files
- `react_web/src/services/chatService.js` - Backend integration
- `react_web/src/components/chat/Sidebar.jsx` - Added health status

### No Changes To
- Backend API (works as-is)
- Frontend UI/UX (same look and feel)
- Authentication system
- Routing

## 💡 Tips

1. **Use Mock Mode for Frontend Development**
   ```env
   VITE_USE_MOCK=true
   ```
   No backend needed!

2. **Check Health Status First**
   Always verify backend is healthy before debugging chat issues

3. **Monitor Network Tab**
   Open DevTools > Network to see API calls

4. **Check Both Consoles**
   Browser console for frontend, terminal for backend

5. **Session Storage**
   DevTools > Application > Session Storage to see session ID

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Main application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| Health Check | http://localhost:8000/api/health | Backend status |

---

## 🚀 Ready to Start?

Run this command and you're good to go:

**Windows:**
```bash
start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh && ./start-dev.sh
```

Then open: **http://localhost:5173**

---

**Happy Chatting! 💬**

For detailed documentation, see the other markdown files in this directory.
