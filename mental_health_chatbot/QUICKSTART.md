# 🚀 Quick Start Guide

Get the Mental Health Chatbot running in 5 minutes!

## Prerequisites Check

```bash
python --version  # Should be 3.11+
pip --version
```

## Step-by-Step Setup

### 1. Navigate to Project

```bash
cd mental_health_chatbot
```

### 2. Create Virtual Environment

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

This will take 5-10 minutes depending on your internet speed.

### 4. Download Models (Optional but Recommended)

**For full ONNX inference:**
```bash
python scripts/download_models.py
```

This takes 15-30 minutes and downloads ~2GB of models.

**Skip this step if you want to test quickly** - the system will use rule-based fallbacks.

### 5. Verify Setup (Optional)

```bash
python scripts/verify_models.py
```

### 6. Start Backend

```bash
cd backend
python main.py
```

You should see:
```
======================================================
Starting Mental Health Chatbot Backend
======================================================
✓ Emotion classifier loaded (ONNX)
✓ Intent classifier loaded (ONNX)
✓ Translation manager initialized
✓ Chat orchestrator initialized
======================================================
Backend startup complete!
Server running at http://0.0.0.0:8000
======================================================
```

### 7. Test the API

Open a new terminal and test:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test1", "message": "I feel sad"}'
```

### 8. Open Test UI

Open `frontend_test/index.html` in your browser.

## Quick Test Without Models

If you want to test immediately without downloading models:

1. Skip step 4 (download models)
2. The system will automatically use rule-based fallbacks
3. You'll see warnings in the logs, but everything will work
4. Responses will be based on keyword matching instead of ML models

## Troubleshooting

### "Module not found" errors

Make sure you're in the virtual environment:
```bash
# Check if (venv) appears in your prompt
# If not, activate it again
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### "Port 8000 already in use"

Change the port in `backend/config.py`:
```python
PORT = 8001  # Or any other available port
```

### Models not loading

Check the logs when starting the server. If you see:
```
⚠ Emotion classifier using rule-based fallback
```

This is normal if you haven't downloaded models. The system will still work!

### Frontend can't connect to backend

1. Make sure backend is running (`python main.py`)
2. Check the URL in `frontend_test/app.js` matches your backend
3. Check browser console for CORS errors

## Next Steps

- Read the full [README.md](README.md) for architecture details
- Check [API documentation](http://localhost:8000/docs) (when server is running)
- Run tests: `cd backend && pytest tests/`
- Try different languages: "मुझे बहुत दुख हो रहा है" (Hindi)

## Demo Script for Hackathon

1. **Show the health endpoint**: http://localhost:8000/api/health
2. **Test normal conversation**: "I'm feeling a bit anxious about my exam"
3. **Show emotion detection**: Watch the metadata in the UI
4. **Test crisis detection**: "I want to end my life" → See immediate helpline response
5. **Test multilingual**: "Je me sens très triste" (French)
6. **Show turn progression**: Have a 5+ turn conversation, watch responses evolve
7. **Show processing speed**: Point out the millisecond timing in metadata

## Support

- Check logs in the terminal where `python main.py` is running
- Visit http://localhost:8000/api/health for system status
- All errors are logged with full stack traces

---

**Ready to demo!** 🎉
