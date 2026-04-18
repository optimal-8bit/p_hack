# 🚀 Quick Start - Doctor Integration

## 3-Step Setup

### 1️⃣ Backend Setup (2 minutes)
```bash
cd mental_health_chatbot/backend

# Seed sample doctors
python seed_doctors.py

# Start server
python main.py
```

### 2️⃣ Frontend Setup (1 minute)
```bash
cd react_web

# Start dev server
npm run dev
```

### 3️⃣ Test It! (1 minute)
1. Open: http://localhost:5173/mental-health-chat
2. Type: "I feel anxious and can't sleep"
3. Continue chatting (3-4 messages)
4. See doctor recommendation appear! 🎉

## What You Get

✅ **AI-Powered Recommendations** - Analyzes symptoms and suggests specialists  
✅ **6 Sample Doctors** - Psychiatrists, psychologists, therapists  
✅ **Smart Urgency Detection** - Crisis cases get immediate attention  
✅ **Beautiful UI** - Recommendations appear naturally in chat  
✅ **Doctor Dashboard** - Manage appointments and patients  

## Test Messages

Try these to trigger recommendations:

**Anxiety:**
- "I've been feeling really anxious"
- "I'm having panic attacks"
- "I can't stop worrying"

**Depression:**
- "I feel sad all the time"
- "I have no energy"
- "Nothing makes me happy"

**Crisis (urgent):**
- "I don't want to live anymore"
- "I want to hurt myself"

## API Endpoints

```bash
# List all doctors
curl http://localhost:8000/api/doctor/search

# Get recommendations for session
curl http://localhost:8000/api/doctor/recommendations/session-123

# Doctor dashboard
curl http://localhost:8000/api/doctor/dashboard?doctor_id=doc-001
```

## Troubleshooting

**No recommendations?**
- Chat at least 3-4 times
- Use symptom keywords (anxious, depressed, panic)
- Check backend logs

**No doctors found?**
- Run: `python seed_doctors.py`

**Import errors?**
- Check: `react_web/src/services/api.service.js` exists
- Restart frontend: `npm run dev`

## Files Created

**Backend:**
- `database/doctor_models.py` - Database schema
- `api/doctor_routes.py` - 10 new endpoints
- `services/doctor_recommendation_service.py` - AI logic
- `seed_doctors.py` - Sample data

**Frontend:**
- `services/api.service.js` - HTTP client
- `components/chat/DoctorRecommendation.jsx` - UI component

## Next Steps

📖 Read: `DOCTOR_INTEGRATION_GUIDE.md` for full documentation  
✅ Check: `SETUP_CHECKLIST.md` for detailed verification  
🧪 Test: `python test_doctor_integration.py` to verify setup  

---

**That's it!** You now have a fully functional doctor recommendation system integrated into your mental health chatbot. 🎊
