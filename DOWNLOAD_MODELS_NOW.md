# Download Backend Models

## Issue
The backend is running but the emotion and intent classifier models are not loaded (showing ✗ in the health status).

## Solution
Run the model download script to get the ONNX models:

```bash
cd p_hack/mental_health_chatbot
source backend/venv/bin/activate
python scripts/download_models.py
```

## What This Does
1. Downloads emotion classifier model (~250MB)
2. Downloads intent classifier model (~100MB)
3. Downloads translation models for Hindi, French, Spanish (~1GB total)
4. Converts classification models to ONNX format for fast inference
5. Takes about 10-20 minutes depending on your internet speed

## After Download
1. The script will show a summary of what was downloaded
2. Restart the backend server (Ctrl+C and run `python backend/main.py` again)
3. Refresh your React frontend
4. The health status should show ✓ for emotion_classifier and intent_classifier
5. Chat will work with full AI-powered emotion and intent detection!

## Current Status
- ✅ Backend server running
- ✅ Frontend connected to backend
- ⏳ Models need to be downloaded
- ⏳ After models are downloaded, restart backend

## Note
The backend will work without models (using rule-based fallbacks), but downloading the models gives you the full AI-powered experience!
