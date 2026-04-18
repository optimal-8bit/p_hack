# Get Doctor Recommendations Working - Step by Step

## The Problem
Doctor recommendations weren't showing up in the frontend chat.

## The Solution
I've fixed the integration and lowered thresholds for easier testing.

## What Changed

### 1. Fixed Conversation Analysis
- **Before:** Only analyzed current message
- **After:** Analyzes full conversation history
- **Impact:** Better symptom detection across multiple messages

### 2. Lowered Thresholds
- **Symptom threshold:** 3 → 2 (easier to trigger)
- **Turn requirement:** 3 → 2 (shows sooner)
- **Impact:** Recommendations appear faster

### 3. Added More Keywords
- Added: "anxious", "panic", "depressed", "sad", "can't sleep", "exhausted"
- **Impact:** Catches more symptom mentions

### 4. Better Logging
- Added detailed logs to track recommendation flow
- **Impact:** Easy to debug if issues occur

## Quick Test (5 minutes)

### Step 1: Verify Files (30 seconds)
```bash
python verify_doctor_setup.py
```

**Expected:** All ✅ checkmarks

### Step 2: Start Backend (1 minute)
```bash
cd mental_health_chatbot/backend

# Seed doctors (run once)
python seed_doctors.py

# Start server
python main.py
```

**Expected:** "Backend startup complete!"

### Step 3: Test Recommendation System (30 seconds)
Open browser:
```
http://localhost:8000/api/test-recommendation
```

**Expected:**
```json
{
  "status": "working",
  "recommendation_generated": true,
  "recommendation": {
    "recommended_specialization": "psychologist",
    "urgency": "normal"
  }
}
```

✅ **If you see this, the backend is working!**

### Step 4: Start Frontend (1 minute)
```bash
cd react_web
npm run dev
```

**Expected:** "Local: http://localhost:5173/"

### Step 5: Test in Chat (2 minutes)
1. Open: http://localhost:5173/mental-health-chat

2. **Type Message 1:**
   ```
   I feel anxious
   ```
   Wait for response...

3. **Type Message 2:**
   ```
   I can't sleep at night
   ```
   Wait for response...

4. **Look for recommendation card below bot's response!**

## What You Should See

After message 2, you should see this appear:

```
┌─────────────────────────────────────────────────────┐
│ 🩺 Professional Support Recommended                 │
│                                                     │
│ Based on what you've shared, speaking with a       │
│ mental health professional could be beneficial...  │
│                                                     │
│ Recommended specialist: Psychologist               │
│                                                     │
│ [Find a Doctor] [Dismiss]                          │
└─────────────────────────────────────────────────────┘
```

Click **"Find a Doctor"** to see the list of psychologists!

## Troubleshooting

### Issue: Still no recommendation

**Check Backend Logs:**

Look for these messages in your terminal:

```
🔍 [DOCTOR-REC] Analyzing conversation: turn=2, messages=2
✅ [DOCTOR-REC] Recommendation generated: specialization=psychologist
🏥 [DOCTOR-REC] Showing recommendation to user
```

**If you see these:** Backend is working, check frontend

**If you DON'T see these:**

1. **Check you're using symptom keywords:**
   - ✅ "anxious", "depressed", "panic", "can't sleep"
   - ❌ "not feeling great", "bad day" (too vague)

2. **Check turn number:**
   - Need at least 2 messages
   - Backend logs show: `turn=2`

3. **Restart backend:**
   ```bash
   # Stop with Ctrl+C
   python main.py
   ```

### Issue: Backend working but not showing in frontend

**Check Browser Console (F12):**

Look for the API response:
```javascript
{
  doctor_recommendation: {
    should_recommend: true,
    specialization: "psychologist"
  }
}
```

**If you see this:** Frontend received it, check component

**If you DON'T see this:**

1. **Check API URL:**
   - Open `react_web/src/services/api.service.js`
   - Verify: `const API_BASE_URL = 'http://localhost:8000'`

2. **Check for CORS errors:**
   - Backend should show: `allow_origins=["*"]`

3. **Restart frontend:**
   ```bash
   # Stop with Ctrl+C
   npm run dev
   ```

### Issue: Component not rendering

**Check files exist:**
```bash
ls react_web/src/components/chat/DoctorRecommendation.jsx
ls react_web/src/services/api.service.js
```

**Check for errors in browser console**

**Restart frontend:**
```bash
npm run dev
```

## Test Messages That Work

### Anxiety (Psychologist)
```
Message 1: "I feel anxious"
Message 2: "I'm having panic attacks"
```

### Depression (Psychologist)
```
Message 1: "I feel depressed"
Message 2: "I have no energy"
```

### Sleep Issues (GP)
```
Message 1: "I can't sleep"
Message 2: "I'm always tired"
```

### Crisis (Psychiatrist - URGENT)
```
Message 1: "I don't want to live anymore"
```
(Shows immediately with red urgent styling)

## Verification Checklist

Run through this checklist:

- [ ] `python verify_doctor_setup.py` shows all ✅
- [ ] Backend starts without errors
- [ ] `http://localhost:8000/api/test-recommendation` returns `recommendation_generated: true`
- [ ] Backend logs show "Backend startup complete!"
- [ ] Frontend starts without errors
- [ ] Chat page loads at `http://localhost:5173/mental-health-chat`
- [ ] Can type and send messages
- [ ] Bot responds to messages
- [ ] After 2 messages with symptoms, backend logs show:
  - `🔍 [DOCTOR-REC] Analyzing conversation`
  - `✅ [DOCTOR-REC] Recommendation generated`
  - `🏥 [DOCTOR-REC] Showing recommendation to user`
- [ ] Recommendation card appears in chat UI
- [ ] "Find a Doctor" button works
- [ ] Doctor list displays

## Success!

If you see the recommendation card in the chat, **you're done!** 🎉

The system is now:
- ✅ Analyzing conversations
- ✅ Detecting symptoms
- ✅ Generating recommendations
- ✅ Displaying in UI
- ✅ Showing doctor lists

## Customize

Now that it's working, you can:

1. **Adjust thresholds** in `doctor_recommendation_service.py`:
   ```python
   self.recommendation_threshold = 2  # Change this
   ```

2. **Add more symptoms** in `SYMPTOM_PATTERNS`

3. **Customize UI** in `DoctorRecommendation.jsx`

4. **Add more doctors** by editing `seed_doctors.py`

## Need More Help?

1. **Read:** `TEST_DOCTOR_RECOMMENDATIONS.md` for detailed testing
2. **Check:** Backend logs for error messages
3. **Verify:** Browser console for frontend errors
4. **Test:** `http://localhost:8000/api/test-recommendation` endpoint

## Quick Commands Reference

```bash
# Verify setup
python verify_doctor_setup.py

# Backend
cd mental_health_chatbot/backend
python seed_doctors.py  # Run once
python main.py          # Start server

# Frontend
cd react_web
npm run dev            # Start dev server

# Test endpoints
curl http://localhost:8000/api/test-recommendation
curl http://localhost:8000/api/doctor/search
curl http://localhost:8000/api/health

# Chat
http://localhost:5173/mental-health-chat
```

---

**Remember:** Type at least 2 messages with symptom keywords like "anxious", "depressed", "can't sleep" to trigger recommendations!
