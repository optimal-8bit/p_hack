# 🧠 Mental Health Chatbot - Offline AI System

An offline, privacy-first, multilingual AI mental health chatbot built for healthcare hackathons. This system runs entirely locally using ONNX-quantized transformer models with **zero cloud LLM calls**.

## 🎯 Key Features

- **100% Offline**: All AI inference runs locally using ONNX models
- **Privacy-First**: No data leaves the device
- **Fast**: Sub-500ms response time on CPU
- **Multilingual**: Supports English, Hindi, French, and Spanish
- **Crisis Detection**: Immediate safety responses with helpline information
- **Context-Aware**: Maintains conversation history for personalized responses
- **No Hallucinations**: Template-based responses ensure safety and reliability

## 🏗️ Architecture

```
User Message
    ↓
[Safety Check] ← Crisis patterns (regex, <5ms)
    ↓
[Preprocessing] ← Text cleaning, language detection
    ↓
[Translation] ← ONNX seq2seq models (if needed)
    ↓
[Emotion Classification] ← ONNX DistilRoBERTa (7 emotions)
    ↓
[Intent Classification] ← ONNX NLI cross-encoder (6 intents)
    ↓
[Context Tracking] ← Last 5 turns, session memory
    ↓
[Response Selection] ← Template matching (emotion × intent × turn)
    ↓
[Translation Back] ← To user's language
    ↓
Response + Metadata
```

## 📋 Prerequisites

- Python 3.11+
- pip
- ~2GB disk space for models
- 4GB+ RAM recommended

## 🚀 Setup Instructions

### 1. Clone and Navigate

```bash
cd mental_health_chatbot
```

### 2. Create Virtual Environment

```bash
# On Linux/Mac
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Download Models

This step downloads and converts all models to ONNX format (~15-30 minutes):

```bash
python scripts/download_models.py
```

**Note**: Translation model exports may fail (known issue with seq2seq ONNX export). The system will automatically fall back to using HuggingFace transformers directly.

### 5. Verify Models

```bash
python scripts/verify_models.py
```

This tests all models with sample inputs and shows which are working.

### 6. Start the Backend

```bash
cd backend
python main.py
```

The server will start at `http://localhost:8000`

### 7. Open Test UI

Open `frontend_test/index.html` in your web browser.

## 📡 API Reference

### POST /api/chat

Send a message to the chatbot.

**Request:**
```json
{
  "session_id": "unique-session-id",
  "message": "I feel really sad and hopeless"
}
```

**Response:**
```json
{
  "response_text": "I can hear that you're going through something really painful...",
  "detected_language": "en",
  "emotion": {
    "emotion": "sadness",
    "confidence": 0.87,
    "all_scores": {...}
  },
  "intent": {
    "intent": "sadness and depression",
    "confidence": 0.79
  },
  "turn_number": 1,
  "is_crisis": false,
  "processing_time_ms": 234.5,
  "session_id": "unique-session-id"
}
```

### GET /api/health

Check system health and model status.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "emotion_classifier": true,
    "intent_classifier": true,
    "translator_hi": true,
    "translator_fr": false
  },
  "version": "1.0.0"
}
```

### GET /api/session/{session_id}/history

Get conversation history for a session.

### DELETE /api/session/{session_id}

Clear in-memory context for a session.

### GET /api/supported-languages

List supported languages.

## 🧪 Testing

The system includes comprehensive tests:

```bash
cd backend
pytest tests/
```

## 🔧 Model Credits

- **Emotion Classification**: [j-hartmann/emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)
- **Intent Classification**: [cross-encoder/nli-MiniLM2-L6-H768](https://huggingface.co/cross-encoder/nli-MiniLM2-L6-H768)
- **Translation**: [Helsinki-NLP OPUS-MT models](https://huggingface.co/Helsinki-NLP)

## 🏆 Hackathon USP

1. **Technical Depth**: Local ML pipeline with ONNX optimization, not just GPT API calls
2. **Safety**: Multi-layer crisis detection with immediate helpline responses
3. **Multilingual**: True multilingual support with automatic language detection
4. **Reliability**: Template-based responses eliminate hallucinations
5. **Privacy**: Zero data transmission, fully offline operation
6. **Performance**: Sub-500ms response time on CPU
7. **Deployability**: Works in low-connectivity environments

## 📊 Performance Metrics

- **Emotion Classification**: ~50-100ms (ONNX) or ~10ms (rule-based)
- **Intent Classification**: ~100-200ms (ONNX) or ~10ms (rule-based)
- **Translation**: ~200-400ms per direction (if needed)
- **Total Pipeline**: <500ms end-to-end on modern laptop CPU

## 🔒 Safety Features

- **Crisis Pattern Detection**: Regex-based detection of suicide, self-harm keywords
- **Immediate Response**: Pre-written crisis responses with helpline numbers
- **Privacy-Safe Logging**: Crisis events logged without message content
- **No Diagnosis**: System never diagnoses mental health conditions
- **Professional Referral**: Suggests professional help in deeper conversations

## 🌍 Supported Languages

- English (en)
- Hindi (hi) - Primary target for Indian hackathon
- French (fr)
- Spanish (es)

## 📝 License

This project is built for educational and hackathon purposes.

## 🆘 Crisis Resources

**India:**
- iCall: 9152987821 (Mon-Sat, 8am-10pm)
- Vandrevala Foundation: 1860-2662-345 (24/7)
- Emergency: 112

## 🤝 Contributing

This is a hackathon project. For production use, please add:
- Authentication and authorization
- Rate limiting
- Enhanced error handling
- Professional mental health expert review
- Comprehensive testing with real users
- HIPAA/GDPR compliance measures

## 📞 Support

For issues or questions, please check:
1. Backend logs: Look for errors in the terminal where `python main.py` is running
2. Health endpoint: Visit `http://localhost:8000/api/health`
3. Model verification: Run `python scripts/verify_models.py`

---

**Built with ❤️ for mental health awareness**
