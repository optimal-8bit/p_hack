# Doctor Integration Setup Checklist

## ✅ Files Created/Modified

### Backend Files Created
- [x] `mental_health_chatbot/backend/database/doctor_models.py` - Database models
- [x] `mental_health_chatbot/backend/api/doctor_routes.py` - API endpoints
- [x] `mental_health_chatbot/backend/services/__init__.py` - Services package
- [x] `mental_health_chatbot/backend/services/doctor_recommendation_service.py` - AI recommendation logic
- [x] `mental_health_chatbot/backend/seed_doctors.py` - Sample data script

### Backend Files Modified
- [x] `mental_health_chatbot/backend/database/db.py` - Added doctor models import
- [x] `mental_health_chatbot/backend/main.py` - Added doctor routes
- [x] `mental_health_chatbot/backend/api/routes.py` - Added recommendation logic
- [x] `mental_health_chatbot/backend/api/schemas.py` - Added recommendation schema

### Frontend Files Created
- [x] `react_web/src/services/api.service.js` - HTTP client
- [x] `react_web/src/components/chat/DoctorRecommendation.jsx` - Recommendation UI

### Frontend Files Modified
- [x] `react_web/src/services/doctor.service.js` - Real API integration
- [x] `react_web/src/components/chat/MessageBubble.jsx` - Display recommendations
- [x] `react_web/src/pages/MentalHealthChatPage.jsx` - Pass recommendations
- [x] `react_web/src/services/chatService.js` - Handle recommendations

### Documentation
- [x] `DOCTOR_INTEGRATION_GUIDE.md` - Complete guide
- [x] `DOCTOR_INTEGRATION_SUMMARY.md` - Implementation details
- [x] `test_doctor_integration.py` - Test script
- [x] `SETUP_CHECKLIST.md` - This file

## 🚀 Setup Steps

### Step 1: Verify Backend Files
```bash
# Check if all backend files exist
ls mental_health_chatbot/backend/database/doctor_models.py
ls mental_health_chatbot/backend/api/doctor_routes.py
ls mental_health_chatbot/backend/services/doctor_recommendation_service.py
ls mental_health_chatbot/backend/seed_doctors.py
```

### Step 2: Install Backend Dependencies
```bash
cd mental_health_chatbot/backend
pip install -r requirements.txt
```

### Step 3: Seed Sample Doctors
```bash
cd mental_health_chatbot/backend
python seed_doctors.py
```

Expected output:
```
Creating database tables...
Seeding sample doctors...
  ✅ Added Dr. Sarah Johnson (psychiatrist)
  ✅ Added Dr. Michael Chen (psychologist)
  ✅ Added Dr. Emily Rodriguez (therapist)
  ✅ Added Dr. James Williams (psychiatrist)
  ✅ Added Dr. Lisa Anderson (psychologist)
  ✅ Added Dr. Robert Taylor (general_practitioner)

✅ Successfully seeded 6 doctors!
```

### Step 4: Start Backend Server
```bash
cd mental_health_chatbot/backend
python main.py
```

Expected output should include:
```
✓ Emotion classifier loaded (ONNX)
✓ Intent classifier loaded (ONNX)
✓ Translation manager initialized
✓ Chat orchestrator initialized
Backend startup complete!
Server running at http://localhost:8000
```

### Step 5: Verify Backend API
Open browser and test:
- http://localhost:8000 - Should show API homepage
- http://localhost:8000/docs - Should show Swagger UI with doctor endpoints
- http://localhost:8000/api/doctor/search - Should return list of doctors

### Step 6: Verify Frontend Files
```bash
# Check if all frontend files exist
ls react_web/src/services/api.service.js
ls react_web/src/services/doctor.service.js
ls react_web/src/components/chat/DoctorRecommendation.jsx
```

### Step 7: Install Frontend Dependencies
```bash
cd react_web
npm install
```

### Step 8: Start Frontend Server
```bash
cd react_web
npm run dev
```

Expected output:
```
VITE v... ready in ...ms

➜  Local:   http://localhost:5173/
```

### Step 9: Test Chat Integration
1. Open http://localhost:5173/mental-health-chat
2. Type messages with symptoms:
   - "I've been feeling really anxious"
   - "I can't sleep at night"
   - "I'm having panic attacks"
3. After 3-4 messages, you should see a doctor recommendation card
4. Click "Find a Doctor" to see available specialists

### Step 10: Test Doctor Dashboard
1. Open http://localhost:5173/doctor-dashboard
2. Should see:
   - Metrics (appointments, patients, prescriptions)
   - Today's appointments
   - Pending appointments
   - AI workload summary

## 🧪 Testing Scenarios

### Test 1: Anxiety Recommendation
**Input:**
```
User: "I've been feeling really anxious lately"
User: "I can't sleep and I'm worried all the time"
User: "I have panic attacks frequently"
```

**Expected:**
- Bot responds with empathy
- After 3rd message, recommendation card appears
- Specialization: "psychologist"
- Urgency: "normal" or "high"
- Shows list of psychologists when "Find a Doctor" clicked

### Test 2: Crisis Detection
**Input:**
```
User: "I don't want to live anymore"
```

**Expected:**
- Immediate crisis response from bot
- Recommendation card with urgency: "urgent"
- Shows crisis hotline (988) button
- Red/urgent styling

### Test 3: Doctor Search
**API Test:**
```bash
curl "http://localhost:8000/api/doctor/search?specialization=psychiatrist"
```

**Expected:**
- Returns list of psychiatrists
- Each has: name, email, specialization, rating, experience

### Test 4: Get Recommendations
**API Test:**
```bash
curl "http://localhost:8000/api/doctor/recommendations/test-session-123"
```

**Expected:**
- Returns empty array (no recommendations yet) or
- Returns recommendations if session has them

## 🐛 Troubleshooting

### Issue: "Module not found: api.service"
**Solution:** File created at `react_web/src/services/api.service.js`
```bash
# Verify it exists
ls react_web/src/services/api.service.js
```

### Issue: "No doctors found"
**Solution:** Run seed script
```bash
cd mental_health_chatbot/backend
python seed_doctors.py
```

### Issue: "Database error"
**Solution:** Check if database file exists
```bash
ls mental_health_chatbot/backend/chat_history.db
# If not, it will be created on first run
```

### Issue: "Doctor routes not found (404)"
**Solution:** Verify doctor routes are registered in main.py
```python
# Should see this in main.py:
from api.doctor_routes import router as doctor_router
app.include_router(doctor_router)
```

### Issue: "No recommendations appearing"
**Solution:** 
1. Check backend logs for errors
2. Verify conversation has 3+ turns
3. Use keywords like "anxious", "depressed", "panic"
4. Check browser console for API errors

### Issue: "CORS errors"
**Solution:** Backend already has CORS enabled for all origins
```python
# In main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

## 📊 Verification Checklist

- [ ] Backend starts without errors
- [ ] Seed script runs successfully
- [ ] API docs accessible at /docs
- [ ] Doctor search returns results
- [ ] Frontend starts without errors
- [ ] Chat page loads
- [ ] Doctor dashboard loads
- [ ] Typing in chat works
- [ ] Bot responds to messages
- [ ] Recommendations appear after 3+ messages
- [ ] "Find a Doctor" button works
- [ ] Doctor list displays
- [ ] Crisis messages show urgent recommendations
- [ ] Dismissing recommendations works

## 🎯 Success Criteria

You'll know everything is working when:

1. ✅ Backend starts and shows "Backend startup complete!"
2. ✅ Seed script adds 6 doctors
3. ✅ Chat responds to your messages
4. ✅ After mentioning anxiety/depression symptoms 3+ times, a recommendation card appears
5. ✅ Clicking "Find a Doctor" shows a list of specialists
6. ✅ Doctor dashboard shows metrics and appointments

## 📞 Quick Commands Reference

```bash
# Backend
cd mental_health_chatbot/backend
python seed_doctors.py          # Seed doctors (run once)
python main.py                  # Start server

# Frontend
cd react_web
npm install                     # Install dependencies (run once)
npm run dev                     # Start dev server

# Testing
curl http://localhost:8000/api/health                    # Check backend health
curl http://localhost:8000/api/doctor/search             # List all doctors
curl http://localhost:8000/api/doctor/dashboard?doctor_id=doc-001  # Doctor dashboard
```

## 🎉 Next Steps After Setup

Once everything is working:

1. **Customize Recommendations**
   - Edit `services/doctor_recommendation_service.py`
   - Adjust symptom patterns and thresholds

2. **Add More Doctors**
   - Edit `seed_doctors.py`
   - Add your own doctor profiles

3. **Enhance UI**
   - Customize `DoctorRecommendation.jsx`
   - Add your branding and styling

4. **Add Authentication**
   - Implement user login
   - Protect doctor routes
   - Add role-based access

5. **Production Deployment**
   - Set up proper database (PostgreSQL)
   - Add environment variables
   - Configure HTTPS
   - Implement HIPAA compliance

## 📚 Documentation

- `DOCTOR_INTEGRATION_GUIDE.md` - Detailed technical guide
- `DOCTOR_INTEGRATION_SUMMARY.md` - Implementation overview
- `test_doctor_integration.py` - Automated test script

---

**Need Help?**
1. Check backend logs for errors
2. Check browser console for frontend errors
3. Review the troubleshooting section above
4. Verify all files exist using the checklist
