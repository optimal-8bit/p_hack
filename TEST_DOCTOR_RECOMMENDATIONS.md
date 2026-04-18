# Testing Doctor Recommendations

## Quick Test Steps

### 1. Start Backend
```bash
cd mental_health_chatbot/backend
python main.py
```

### 2. Test Recommendation System
Open browser and go to:
```
http://localhost:8000/api/test-recommendation
```

**Expected Response:**
```json
{
  "status": "working",
  "recommendation_generated": true,
  "recommendation": {
    "session_id": "test-session",
    "recommended_specialization": "psychologist",
    "reason": "...",
    "urgency": "normal",
    "symptoms": ["anxious", "can't sleep", "worried"],
    "is_crisis": false
  },
  "threshold": 2,
  "message": "Doctor recommendation system is operational"
}
```

### 3. Test in Chat

**Start Frontend:**
```bash
cd react_web
npm run dev
```

**Open Chat:**
```
http://localhost:5173/mental-health-chat
```

**Test Messages (Type these in order):**

**Message 1:**
```
I've been feeling really anxious lately
```

**Message 2:**
```
I can't sleep at night and I'm worried all the time
```

**Message 3:**
```
I'm having panic attacks and feel overwhelmed
```

**Expected Result:**
After message 2 or 3, you should see a blue recommendation card appear below the bot's response:

```
┌─────────────────────────────────────────────┐
│ 🩺 Professional Support Recommended         │
│                                             │
│ Based on what you've shared, speaking with │
│ a mental health professional could be       │
│ beneficial...                               │
│                                             │
│ Recommended specialist: Psychologist        │
│                                             │
│ [Find a Doctor]                             │
└─────────────────────────────────────────────┘
```

## Test Scenarios

### Scenario 1: Anxiety (Normal Urgency)
```
Message 1: "I feel anxious"
Message 2: "I'm worried all the time"
Message 3: "I have panic attacks"
```
**Expected:** Psychologist recommendation, normal urgency (blue)

### Scenario 2: Depression (Normal Urgency)
```
Message 1: "I feel sad"
Message 2: "I have no energy"
Message 3: "Nothing makes me happy anymore"
```
**Expected:** Psychologist recommendation, normal urgency (blue)

### Scenario 3: Sleep Issues (Normal Urgency)
```
Message 1: "I can't sleep"
Message 2: "I'm always tired"
Message 3: "I have insomnia"
```
**Expected:** General Practitioner recommendation, normal urgency (blue)

### Scenario 4: Crisis (Urgent)
```
Message 1: "I don't want to live anymore"
```
**Expected:** Psychiatrist recommendation, URGENT (red), shows crisis hotline

### Scenario 5: Severe Symptoms (High Urgency)
```
Message 1: "I'm severely depressed"
Message 2: "I can't get out of bed"
Message 3: "I feel hopeless"
```
**Expected:** Psychiatrist recommendation, high urgency (yellow)

## Debugging

### Check Backend Logs

Look for these log messages:

**When analyzing:**
```
🔍 [DOCTOR-REC] Analyzing conversation: turn=2, messages=2, emotions=['anxiety', 'fear'], is_crisis=False
```

**When recommendation generated:**
```
✅ [DOCTOR-REC] Recommendation generated: specialization=psychologist, urgency=normal, symptoms=3
```

**When showing to user:**
```
🏥 [DOCTOR-REC] Showing recommendation to user: psychologist (urgency: normal)
```

**When not showing yet:**
```
⏭️ [DOCTOR-REC] Recommendation generated but not shown yet (turn 1)
```

**When no recommendation:**
```
ℹ️ [DOCTOR-REC] No recommendation needed yet (turn 1, symptoms below threshold)
```

### Check Frontend Console

Open browser DevTools (F12) and look for:

**When recommendation received:**
```javascript
{
  doctor_recommendation: {
    should_recommend: true,
    specialization: "psychologist",
    reason: "...",
    urgency: "normal"
  }
}
```

### Common Issues

#### Issue 1: No recommendation appearing

**Check:**
1. Backend logs show recommendation generated?
2. Frontend console shows `doctor_recommendation` in response?
3. Are you chatting at least 2 times?
4. Are you using symptom keywords?

**Solution:**
```bash
# Test the endpoint directly
curl http://localhost:8000/api/test-recommendation

# Check if it returns recommendation_generated: true
```

#### Issue 2: Recommendation generated but not shown

**Possible causes:**
- Turn number < 2
- `should_show_recommendation` returning false

**Check backend logs for:**
```
⏭️ [DOCTOR-REC] Recommendation generated but not shown yet (turn 1)
```

**Solution:** Chat one more time

#### Issue 3: Symptoms not detected

**Check if you're using the right keywords:**

**Good keywords:**
- anxious, anxiety, panic, worried, stress
- depressed, sad, hopeless, worthless
- can't sleep, insomnia, tired, exhausted
- suicidal, suicide, kill myself (crisis)

**Not detected:**
- "I'm not feeling great" (too vague)
- "Having a bad day" (too general)

#### Issue 4: Frontend not displaying recommendation

**Check:**
1. `DoctorRecommendation.jsx` component exists
2. `MessageBubble.jsx` imports and uses it
3. Browser console for errors

**Verify component:**
```bash
ls react_web/src/components/chat/DoctorRecommendation.jsx
```

## API Testing

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "message": "I feel anxious and cant sleep"
  }'
```

**Look for in response:**
```json
{
  "doctor_recommendation": {
    "should_recommend": true,
    "specialization": "psychologist",
    "reason": "...",
    "urgency": "normal"
  }
}
```

### Test Doctor Search
```bash
curl http://localhost:8000/api/doctor/search?specialization=psychologist
```

**Expected:** List of psychologists

### Test Recommendations Endpoint
```bash
curl http://localhost:8000/api/doctor/recommendations/test-123
```

**Expected:** List of recommendations for that session

## Configuration

### Adjust Thresholds

Edit `mental_health_chatbot/backend/services/doctor_recommendation_service.py`:

```python
def __init__(self):
    self.recommendation_threshold = 2  # Change this (default: 2)
```

**Lower = More recommendations**
**Higher = Fewer recommendations**

### Adjust Turn Requirement

```python
def should_show_recommendation(self, turn_number, has_existing_recommendation):
    return turn_number >= 2  # Change this (default: 2)
```

### Add More Symptoms

```python
SYMPTOM_PATTERNS = {
    "psychologist": [
        "anxiety", "panic",
        "your_new_keyword",  # Add here
        # ...
    ]
}
```

## Success Checklist

- [ ] Backend starts without errors
- [ ] Test endpoint returns `recommendation_generated: true`
- [ ] Backend logs show recommendation analysis
- [ ] Chat responds to messages
- [ ] After 2-3 messages with symptoms, recommendation appears
- [ ] Recommendation card is visible in UI
- [ ] "Find a Doctor" button works
- [ ] Doctor list displays when clicked
- [ ] Crisis messages show urgent (red) recommendations

## Expected Behavior

### Turn 1
```
User: "I feel anxious"
Bot: "I understand you're feeling anxious..."
[No recommendation yet - turn 1]
```

### Turn 2
```
User: "I can't sleep"
Bot: "Sleep problems can be difficult..."
[Recommendation appears! - turn 2, 2+ symptoms detected]

┌─────────────────────────────────────┐
│ 🩺 Professional Support Recommended │
│ Recommended: Psychologist           │
│ [Find a Doctor]                     │
└─────────────────────────────────────┘
```

## Verification Commands

```bash
# 1. Check backend is running
curl http://localhost:8000/api/health

# 2. Test recommendation system
curl http://localhost:8000/api/test-recommendation

# 3. Check doctors exist
curl http://localhost:8000/api/doctor/search

# 4. Test chat with symptoms
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"I feel anxious and depressed"}'

# 5. Check frontend is running
curl http://localhost:5173
```

## Next Steps

Once recommendations are working:

1. **Customize Messages**
   - Edit `_generate_reason()` in `doctor_recommendation_service.py`

2. **Add More Specializations**
   - Add to `SYMPTOM_PATTERNS` dictionary

3. **Adjust Urgency**
   - Modify `URGENCY_EMOTIONS` dictionary

4. **Style Recommendations**
   - Edit `DoctorRecommendation.jsx` component

5. **Add More Doctors**
   - Edit and run `seed_doctors.py`
