# Verify LLM Integration

## ✅ Quick Verification Steps

### Step 1: Check Config (5 seconds)

Open: `mental_health_chatbot/backend/config.py`

Look for:
```python
LLM_ENABLED = True  # Should be True
LLM_TIMEOUT = 30.0  # Should be 30.0
LLM_MAX_TOKENS = 200  # Should be 200
```

### Step 2: Restart Backend (10 seconds)

```bash
# Stop current backend (Ctrl+C)

# Start backend
cd mental_health_chatbot/backend
python main.py
```

**Watch for these logs:**
```
INFO: Starting Mental Health Chatbot Backend
INFO: Creating database tables...
INFO: Loading emotion classifier...
INFO: Loading intent classifier...
INFO: Backend startup complete!
```

### Step 3: Test Upload (30 seconds)

1. Open frontend: http://localhost:5173
2. Click pill icon (💊)
3. Upload any image
4. Click "Analyze Prescription"
5. **WAIT** - You should see loading for 2-30 seconds
6. Check backend terminal

**Expected backend logs:**
```
INFO: Received prescription upload for session: ...
INFO: Starting OCR text extraction...
INFO: Starting prescription analysis...
INFO: Attempting LLM-based extraction...
INFO: Loading Phi-3 Mini for prescription analysis...
INFO: 🚀 Using GPU for prescription analysis
   OR
INFO: ⚠️ Using CPU for prescription analysis (will take 20-30 seconds)
INFO: Model loaded on: CUDA (or CPU)
INFO: Starting LLM generation for prescription analysis...
INFO: Generating with model...
INFO: Generated XXX characters
INFO: LLM generation completed in X.Xs
INFO: Successfully extracted X medicines
INFO: LLM extracted X medicines
```

### Step 4: Verify Results

**If you see:**
- ✅ "Loading Phi-3 Mini" → LLM is loading
- ✅ "LLM generation completed in X.Xs" → LLM is working
- ✅ "Successfully extracted X medicines" → Extraction worked
- ✅ Processing took 2-30 seconds → Real processing

**If you see:**
- ❌ "Using mock medicine data" → LLM failed, using fallback
- ❌ Instant results (<1 second) → LLM not running
- ❌ No "Loading Phi-3" message → LLM not enabled

## 🔍 Detailed Verification

### Check 1: LLM Module Exists

```bash
ls mental_health_chatbot/backend/utils/prescription_llm.py
```

Should show: `prescription_llm.py`

### Check 2: Dependencies Installed

```bash
pip list | grep transformers
pip list | grep torch
```

Should show:
```
transformers    X.X.X
torch           X.X.X
```

If not installed:
```bash
pip install transformers torch
```

### Check 3: Config is Correct

```bash
grep "LLM_ENABLED" mental_health_chatbot/backend/config.py
```

Should show:
```python
LLM_ENABLED = True  # Enabled for prescription analysis
```

### Check 4: Backend Imports Module

Check backend logs for:
```
INFO: Loading Phi-3 Mini for prescription analysis...
```

If you see this, the module is imported and working!

## 🎯 Success Indicators

### ✅ LLM is Working If:

1. **Backend logs show:**
   - "Loading Phi-3 Mini for prescription analysis"
   - "LLM generation completed in X.Xs"
   - "Successfully extracted X medicines"

2. **Processing takes time:**
   - GPU: 2-5 seconds (first time: ~10s)
   - CPU: 20-30 seconds (first time: ~40s)

3. **Frontend shows:**
   - Loading indicator during "Analyzing..."
   - Results appear after delay

4. **Browser console shows:**
   - "Upload response status: 200"
   - "Upload successful: {...}"

### ❌ LLM is NOT Working If:

1. **Backend logs show:**
   - "Using mock medicine data"
   - "LLM extraction failed"
   - No "Loading Phi-3" message

2. **Processing is instant:**
   - Results appear in <1 second
   - No loading delay

3. **Always same medicines:**
   - Always Aspirin, Vitamin D, Metformin
   - Never changes

## 🐛 Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'transformers'"

**Solution:**
```bash
pip install transformers torch
```

### Issue 2: "Using mock medicine data" in logs

**Causes:**
- LLM_ENABLED = False in config
- Transformers not installed
- Model failed to load
- LLM timeout

**Solution:**
1. Check config: `LLM_ENABLED = True`
2. Install dependencies: `pip install transformers torch`
3. Check backend logs for error messages
4. Increase timeout if needed

### Issue 3: Very slow (30+ seconds)

**Cause:** Running on CPU

**This is normal!** CPU processing takes 20-30 seconds.

**Options:**
- Use GPU for faster processing
- Or disable LLM: `LLM_ENABLED = False`

### Issue 4: "CUDA out of memory"

**Cause:** GPU doesn't have enough memory

**Solution:**
```python
# In config.py, disable LLM or use CPU
LLM_ENABLED = False
```

## 📊 Performance Expectations

### First Upload (Cold Start):
- **GPU:** ~10 seconds (model loading + generation)
- **CPU:** ~40 seconds (model loading + generation)

### Subsequent Uploads (Warm):
- **GPU:** 2-5 seconds (generation only)
- **CPU:** 20-30 seconds (generation only)

### Mock Data (Fallback):
- **Always:** <100ms (instant)

## ✨ Final Check

Run this complete test:

1. ✅ Restart backend
2. ✅ Watch logs for "Loading Phi-3 Mini"
3. ✅ Upload prescription in frontend
4. ✅ Wait 2-30 seconds
5. ✅ Check logs for "LLM generation completed"
6. ✅ Verify medicines appear
7. ✅ Create schedule
8. ✅ View reminders

If all steps work → **LLM integration is successful!** 🎉

## 🚀 Quick Test Command

```bash
# In one terminal - Start backend
cd mental_health_chatbot/backend
python main.py

# Watch for:
# "Loading Phi-3 Mini for prescription analysis..."
# "Model loaded on: CUDA" or "Model loaded on: CPU"

# Then test upload in frontend
```

## 📝 Summary

**What to expect:**
- ✅ Backend logs show LLM processing
- ✅ Processing takes 2-30 seconds (not instant)
- ✅ Loading indicator shows in frontend
- ✅ Real medicine extraction (or fallback to mock)

**If something's wrong:**
- Check backend logs for errors
- Verify config: `LLM_ENABLED = True`
- Install dependencies: `pip install transformers torch`
- See troubleshooting section above

**Need help?**
- Check `PRESCRIPTION_LLM_INTEGRATION.md` for details
- Check backend logs for specific errors
- Verify all files are updated
