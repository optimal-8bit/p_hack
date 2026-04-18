# How to Install Models (Emotion & Intent)

This guide shows you how to install the AI models used for emotion detection and intent classification.

## Quick Install (Recommended)

### Step 1: Navigate to the project directory
```bash
cd mental_health_chatbot
```

### Step 2: Run the download script
```bash
python scripts/download_models.py
```

That's it! The script will:
- Download emotion classifier (j-hartmann/emotion-english-distilroberta-base)
- Download intent classifier (cross-encoder/nli-MiniLM2-L6-H768)
- Download translation models for Hindi, French, Spanish
- Convert models to ONNX format for faster inference
- Save them to `backend/onnx_models/`

**Time**: 10-20 minutes  
**Space**: ~1.5GB disk space  
**Internet**: Required for download

## What You'll See

```
============================================================
Mental Health Chatbot - Model Download Script
============================================================

This script will:
1. Export classification models to ONNX (emotion + intent)
2. Download translation models to cache (transformers format)

This may take 10-20 minutes and requires ~1.5GB of disk space.

✓ optimum package is installed

============================================================
PHASE 1: Classification Models (ONNX Export)
============================================================

============================================================
Downloading: Emotion Classifier
Model ID: j-hartmann/emotion-english-distilroberta-base
Output: ../backend/onnx_models/emotion_classifier
============================================================
Loading model from HuggingFace...
Saving ONNX model to backend/onnx_models/emotion_classifier...
Saving tokenizer...
✓ Successfully exported Emotion Classifier (255.3 MB)

============================================================
Downloading: Intent Classifier (NLI)
Model ID: cross-encoder/nli-MiniLM2-L6-H768
Output: ../backend/onnx_models/intent_classifier
============================================================
Loading model from HuggingFace...
Saving ONNX model to backend/onnx_models/intent_classifier...
Saving tokenizer...
✓ Successfully exported Intent Classifier (89.7 MB)

============================================================
PHASE 2: Translation Models (Transformers Cache)
============================================================

[Downloads Hindi, French, Spanish translation models...]

============================================================
DOWNLOAD SUMMARY
============================================================

Classification Models (ONNX):
  ✓ SUCCESS: Emotion Classifier
  ✓ SUCCESS: Intent Classifier (NLI)

Translation Models (Transformers):
  ✓ SUCCESS: Hindi → English Translation
  ✓ SUCCESS: English → Hindi Translation
  ✓ SUCCESS: French → English Translation
  ✓ SUCCESS: English → French Translation
  ✓ SUCCESS: Spanish → English Translation
  ✓ SUCCESS: English → Spanish Translation

Total: 8/8 models successfully processed

✓ All critical models (emotion + intent) are ready!
  → ONNX models exported successfully
  → Translation will use transformers at runtime

The server can now run with full functionality.
```

## Verify Installation

After downloading, verify the models are installed:

```bash
cd mental_health_chatbot
python scripts/verify_models.py
```

You should see:
```
✓ Emotion Classifier: LOADED
✓ Intent Classifier: LOADED
✓ Translation models: AVAILABLE
```

## Troubleshooting

### Error: "optimum package not found"

The script will try to install it automatically. If it fails:

```bash
pip install optimum[onnxruntime]
```

### Error: "No module named 'transformers'"

Install dependencies:

```bash
cd mental_health_chatbot/backend
pip install -r requirements.txt
```

### Error: "Out of disk space"

You need at least 2GB free space. Check with:

```bash
# Windows
dir

# Linux/Mac
df -h
```

### Error: "Connection timeout"

Your internet connection may be slow. The models are large (~1.5GB total). Try:
- Using a faster internet connection
- Running the script again (it will resume)
- Downloading one model at a time (see Manual Install below)

### Models download but server still shows "not loaded"

Check the directory structure:

```bash
# Should see these directories:
mental_health_chatbot/backend/onnx_models/emotion_classifier/
mental_health_chatbot/backend/onnx_models/intent_classifier/

# Each should contain:
- model.onnx
- config.json
- tokenizer files
```

## Manual Install (Alternative)

If the automatic script fails, you can download models manually:

### Step 1: Install Python packages
```bash
cd mental_health_chatbot/backend
pip install -r requirements.txt
pip install optimum[onnxruntime]
```

### Step 2: Download Emotion Model
```python
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

# Download and convert to ONNX
model = ORTModelForSequenceClassification.from_pretrained(
    "j-hartmann/emotion-english-distilroberta-base",
    export=True
)

# Save to correct location
model.save_pretrained("backend/onnx_models/emotion_classifier")

# Save tokenizer
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
tokenizer.save_pretrained("backend/onnx_models/emotion_classifier")
```

### Step 3: Download Intent Model
```python
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

# Download and convert to ONNX
model = ORTModelForSequenceClassification.from_pretrained(
    "cross-encoder/nli-MiniLM2-L6-H768",
    export=True
)

# Save to correct location
model.save_pretrained("backend/onnx_models/intent_classifier")

# Save tokenizer
tokenizer = AutoTokenizer.from_pretrained("cross-encoder/nli-MiniLM2-L6-H768")
tokenizer.save_pretrained("backend/onnx_models/intent_classifier")
```

### Step 4: Download Translation Models (Optional)
```python
from transformers import MarianMTModel, MarianTokenizer

# These will be cached automatically
models = [
    "Helsinki-NLP/opus-mt-hi-en",
    "Helsinki-NLP/opus-mt-en-hi",
    "Helsinki-NLP/opus-mt-fr-en",
    "Helsinki-NLP/opus-mt-en-fr",
    "Helsinki-NLP/opus-mt-es-en",
    "Helsinki-NLP/opus-mt-en-es",
]

for model_id in models:
    print(f"Downloading {model_id}...")
    MarianMTModel.from_pretrained(model_id)
    MarianTokenizer.from_pretrained(model_id)
```

## Do I Need All Models?

### Required (Critical)
- ✅ **Emotion Classifier** - Detects 7 emotions
- ✅ **Intent Classifier** - Detects 6 intent categories

Without these, the backend will use rule-based fallbacks (less accurate).

### Optional (Enhanced Features)
- ⭐ **Translation Models** - For Hindi, French, Spanish support

Without these, the chatbot will only work in English.

## Running Without Models

The backend can run without models! It will use rule-based fallbacks:

**Emotion Detection**: Simple keyword matching
- "happy" → joy
- "sad" → sadness
- "angry" → anger
- etc.

**Intent Classification**: Pattern matching
- "anxious" → anxiety and panic
- "depressed" → sadness and depression
- etc.

**Translation**: English only

This is fine for testing, but models provide much better accuracy.

## Model Sizes

| Model | Size | Purpose |
|-------|------|---------|
| Emotion Classifier | ~255 MB | Detect 7 emotions |
| Intent Classifier | ~90 MB | Detect 6 intents |
| Hindi Translation | ~300 MB | Hindi ↔ English |
| French Translation | ~300 MB | French ↔ English |
| Spanish Translation | ~300 MB | Spanish ↔ English |
| **Total** | **~1.5 GB** | All features |

## Where Are Models Stored?

### ONNX Models (Emotion & Intent)
```
mental_health_chatbot/backend/onnx_models/
├── emotion_classifier/
│   ├── model.onnx
│   ├── config.json
│   └── tokenizer files
└── intent_classifier/
    ├── model.onnx
    ├── config.json
    └── tokenizer files
```

### Translation Models (Transformers Cache)
```
# Windows
C:\Users\<username>\.cache\huggingface\hub\

# Linux/Mac
~/.cache/huggingface/hub/
```

## Checking Model Status

### From UI
1. Start the backend: `python backend/main.py`
2. Start the frontend: `npm run dev` (in react_web/)
3. Open http://localhost:5173
4. Check sidebar "Backend Status" section
5. Should show all models with ✓ checkmarks

### From API
```bash
curl http://localhost:8000/api/health
```

Response:
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

### From Command Line
```bash
cd mental_health_chatbot
python scripts/verify_models.py
```

## Quick Reference

```bash
# Install models (recommended)
cd mental_health_chatbot
python scripts/download_models.py

# Verify installation
python scripts/verify_models.py

# Check model status (backend must be running)
curl http://localhost:8000/api/health

# Start backend
cd backend
python main.py

# Check backend logs for model loading
# Should see:
# ✓ Emotion classifier loaded (ONNX)
# ✓ Intent classifier loaded (ONNX)
```

## FAQ

**Q: How long does it take?**  
A: 10-20 minutes depending on internet speed.

**Q: Can I skip translation models?**  
A: Yes! Only download emotion and intent classifiers. The chatbot will work in English only.

**Q: Do I need GPU?**  
A: No! Models work on CPU. GPU is optional for faster inference.

**Q: Can I use the chatbot while downloading?**  
A: No, download models first, then start the backend.

**Q: What if download fails?**  
A: Run the script again. It will resume from where it stopped.

**Q: Can I delete models later?**  
A: Yes, delete the `backend/onnx_models/` directory. The backend will use fallbacks.

**Q: How do I update models?**  
A: Delete the model directories and run the download script again.

---

## Next Steps

After installing models:

1. ✅ Verify models: `python scripts/verify_models.py`
2. ✅ Start backend: `cd backend && python main.py`
3. ✅ Start frontend: `cd react_web && npm run dev`
4. ✅ Open http://localhost:5173
5. ✅ Check health status shows all models loaded
6. ✅ Test chat with "I'm feeling anxious"

---

**Need Help?** Check `START_HERE.md` or `INTEGRATION_GUIDE.md`
