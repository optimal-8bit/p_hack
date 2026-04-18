# Developer Guide - Advanced Response Engine

## Quick Reference for Developers

### 🚀 Getting Started

#### Run Component Tests
```bash
cd mental_health_chatbot
python test_advanced_components.py
```

#### Run Full Integration Tests (requires venv)
```bash
cd mental_health_chatbot
source venv/bin/activate  # Windows: venv\Scripts\activate
python test_advanced_response_engine.py
```

#### Start the Backend
```bash
cd mental_health_chatbot/backend
uvicorn main:app --reload
```

---

## 📁 Key Files to Know

### Core Response Engine
- **`advanced_response_builder.py`** - Main response builder with all intelligence
- **`reflection.py`** - Pattern-based reflection generation
- **`template_selector.py`** - Integrates advanced builder into pipeline
- **`orchestrator.py`** - Main pipeline coordinator

### Configuration
- **`config.py`** - All system configuration
- Adjust thresholds here for emotion confidence, turn numbers, etc.

### Testing
- **`test_advanced_components.py`** - Unit tests for individual components
- **`test_advanced_response_engine.py`** - Integration tests for full pipeline

---

## 🔧 Common Modifications

### Adjust Emotion Confidence Threshold
**File**: `backend/response_engine/advanced_response_builder.py`
```python
# Line ~140
if emotion_confidence < 0.75:  # Change this value (0.0 to 1.0)
    emotion = "uncertain"
```

### Adjust Professional Help Turn Threshold
**File**: `backend/response_engine/advanced_response_builder.py`
```python
# Line ~195
if turn_number < 4:  # Change minimum turns before suggesting help
    return False
```

### Adjust Short Input Threshold
**File**: `backend/response_engine/advanced_response_builder.py`
```python
# Line ~165
is_short_input = len(user_text.split()) <= 3  # Change word count
```

### Adjust Language Detection Confidence
**File**: `backend/pipeline/preprocessor.py`
```python
# Line ~50
if detected_lang != "en" and lang_confidence >= 0.6:  # Change threshold
    # Translate
```

### Add New Reflection Patterns
**File**: `backend/response_engine/reflection.py`
```python
# Add to TRANSFORMATION_RULES list (Line ~15)
TRANSFORMATION_RULES = [
    # Add your pattern here
    (r"your_regex_pattern", "your reflection template"),
    # Existing patterns...
]
```

### Add New Validation Variants
**File**: `backend/response_engine/advanced_response_builder.py`
```python
# Line ~30
VALIDATION_VARIANTS = [
    "Your new validation phrase.",
    # Existing variants...
]
```

---

## 🐛 Debugging Tips

### Enable Debug Logging
**File**: `backend/main.py`
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # Change from INFO to DEBUG
```

### Check Response Builder State
```python
from response_engine.advanced_response_builder import get_advanced_response_builder

builder = get_advanced_response_builder()
print(builder.session_data)  # See all session data
```

### Test Individual Components
```python
# Test reflection
from response_engine.reflection import generate_reflection
reflection = generate_reflection("I feel sad", "sadness")
print(reflection)

# Test depth detection
from response_engine.advanced_response_builder import DepthDetector
detector = DepthDetector()
intensity = detector.detect_intensity("I can't go on")
print(intensity)  # Should be "high"
```

### Clear Session Data
```python
from pipeline.context_tracker import get_context_tracker
tracker = get_context_tracker()
tracker.clear_session("session_id")
```

---

## 🧪 Testing Checklist

Before deploying changes:

- [ ] Run `python test_advanced_components.py` - All tests pass
- [ ] Run `python test_advanced_response_engine.py` - Integration tests pass
- [ ] Test crisis detection still works
- [ ] Test multilingual support (if modified)
- [ ] Check response latency (<500ms total)
- [ ] Verify no fake personalization
- [ ] Test short input handling
- [ ] Test professional help gating
- [ ] Review logs for errors
- [ ] Test with frontend UI

---

## 📊 Monitoring in Production

### Health Check
```bash
curl http://localhost:8000/health
```

### Check Processing Time
Look for this in logs:
```
INFO: Processed message in XXXms
```
Should be <500ms total.

### Check Crisis Events
```python
from database.db import get_crisis_events
events = await get_crisis_events("session_id")
```

### Monitor Session Count
```python
from pipeline.context_tracker import get_context_tracker
tracker = get_context_tracker()
print(len(tracker.sessions))  # Number of active sessions
```

---

## 🔒 Safety Guidelines

### NEVER Modify These Files
- ❌ `backend/pipeline/safety.py` - Crisis detection
- ❌ `backend/models/emotion_classifier.py` - Emotion model
- ❌ `backend/models/intent_classifier.py` - Intent model
- ❌ `backend/database/models.py` - Database schema
- ❌ `backend/api/schemas.py` - API contracts

### Always Preserve
- ✅ Crisis detection runs first
- ✅ Template-based responses (no LLM generation)
- ✅ No medical advice or diagnosis
- ✅ Professional help suggestions are gated
- ✅ All responses are empathetic

---

## 🎯 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Total Response Time | <500ms | ~300ms |
| Advanced Builder Overhead | <50ms | ~10-20ms |
| Safety Check | <5ms | ~2ms |
| Emotion Classification | <100ms | ~50ms |
| Intent Classification | <100ms | ~50ms |
| Memory per Session | <1MB | ~500KB |

---

## 🔄 Common Workflows

### Adding a New Emotion
1. Add to emotion classifier output (if using custom model)
2. Add validation variants in `advanced_response_builder.py`
3. Add reflection patterns in `reflection.py`
4. Add templates in `templates.py`
5. Test with component tests

### Adding a New Language
1. Add language code to `config.py` → `SUPPORTED_LANGUAGES`
2. Add translation model directory to `TRANSLATION_MODEL_DIRS`
3. Download translation models with `scripts/download_models.py`
4. Test with multilingual inputs

### Adjusting Response Tone
1. Modify validation variants in `advanced_response_builder.py`
2. Adjust reflection patterns in `reflection.py`
3. Update gentle guidance phrases
4. Test with various inputs

---

## 📚 Architecture Overview

```
User Input
    ↓
[Safety Check] ← ALWAYS FIRST
    ↓
[Preprocessing] ← Language detection + translation
    ↓
[Emotion Classification] ← ONNX model + confidence
    ↓
[Intent Classification] ← ONNX model
    ↓
[Context Tracking] ← Last 5 turns
    ↓
[Template Selector] ← Integrates advanced builder
    ↓
[Advanced Response Builder]
    ├─ Confidence Check
    ├─ Trajectory Analysis
    ├─ Depth Detection
    ├─ Component Building
    │   ├─ Validation
    │   ├─ Reflection
    │   ├─ Normalization
    │   ├─ Coping
    │   ├─ Guidance
    │   └─ Question
    ├─ Flow Selection
    ├─ Assembly
    └─ Professional Help Gating
    ↓
[Translation Back] ← If needed
    ↓
Response to User
```

---

## 🆘 Troubleshooting

### "No module named 'transformers'"
```bash
pip install transformers
```

### "No module named 'langdetect'"
```bash
pip install langdetect
```

### "ONNX model not found"
```bash
cd mental_health_chatbot
python scripts/download_models.py
```

### "Session data growing too large"
```python
# Reduce context window size in config.py
CONTEXT_WINDOW_SIZE = 3  # Default is 5
```

### "Responses are too similar"
- Check variation engine is working
- Increase number of variants
- Verify session_id is unique per user

### "Professional help suggested too early"
- Check turn_number is being passed correctly
- Verify gating logic in `ProfessionalHelpGating`
- Review trajectory analysis

---

## 📖 Further Reading

- **`ADVANCED_RESPONSE_ENGINE.md`** - Comprehensive feature documentation
- **`PHASE2_COMPLETION_SUMMARY.md`** - Implementation summary
- **`PROJECT_SUMMARY.md`** - Overall project overview
- **`QUICKSTART.md`** - Setup instructions
- **`README.md`** - Project introduction

---

## 💡 Tips for Contributors

1. **Always test locally first** - Run component tests before committing
2. **Preserve safety** - Never modify safety.py or bypass safety checks
3. **Document changes** - Update relevant .md files
4. **Follow patterns** - Use existing code style and patterns
5. **Think deterministic** - Avoid randomness in logic, only in variation
6. **Consider edge cases** - Test with short inputs, long inputs, crisis scenarios
7. **Monitor performance** - Keep latency under targets
8. **Write tests** - Add tests for new features

---

## 🤝 Getting Help

### Check Logs
```bash
# Backend logs show detailed processing
tail -f backend/logs/app.log  # If logging to file
```

### Run Diagnostics
```bash
python scripts/verify_models.py  # Check model status
```

### Review Test Output
```bash
python test_advanced_components.py -v  # Verbose output
```

---

**Happy Coding!** 🚀

*Remember: This is a mental health application. Every line of code impacts real people. Code with care and empathy.* 💚