# Doctor Integration Guide

## Overview

The doctor integration connects the mental health chatbot with a professional healthcare system. When the AI detects concerning symptoms or patterns during conversations, it can recommend professional help and connect users with qualified mental health professionals.

## Features

### 1. **AI-Powered Doctor Recommendations**
- Analyzes conversation patterns, emotions, and symptoms
- Determines urgency level (low, normal, high, urgent)
- Recommends appropriate specialist types (psychiatrist, psychologist, therapist, GP)
- Provides contextual reasons for recommendations

### 2. **Doctor Management System**
- Doctor profiles with specializations, ratings, and experience
- Patient management and appointment tracking
- Prescription management
- Dashboard with AI-powered workload summaries

### 3. **Seamless Chat Integration**
- Doctor recommendations appear naturally in chat conversations
- Users can browse and contact recommended doctors directly
- Crisis situations trigger urgent recommendations with hotline access

## Backend Architecture

### Database Models (`database/doctor_models.py`)

```python
- Doctor: Professional profiles with specializations
- Patient: User health profiles
- Appointment: Scheduling and status tracking
- Prescription: Medication management
- DoctorRecommendation: AI-generated recommendations linked to chat sessions
```

### API Routes (`api/doctor_routes.py`)

```
GET  /api/doctor/dashboard?doctor_id={id}          # Doctor dashboard
GET  /api/doctor/appointments?doctor_id={id}       # List appointments
POST /api/doctor/appointments                      # Create appointment
PATCH /api/doctor/appointments/{id}                # Update appointment
GET  /api/doctor/patients?doctor_id={id}           # List patients
GET  /api/doctor/prescriptions?doctor_id={id}      # List prescriptions
GET  /api/doctor/recommendations/{session_id}      # Get recommendations
GET  /api/doctor/search?specialization=...         # Search doctors
```

### Recommendation Service (`services/doctor_recommendation_service.py`)

The recommendation engine analyzes:
- **Symptom patterns**: Keywords indicating mental health concerns
- **Emotion trends**: Persistent negative emotions
- **Crisis indicators**: Suicidal ideation, self-harm mentions
- **Conversation context**: Turn count, intent patterns

**Urgency Levels:**
- `urgent`: Crisis situations requiring immediate intervention
- `high`: Severe symptoms needing prompt attention
- `normal`: General mental health concerns
- `low`: Preventive care or mild symptoms

## Frontend Integration

### Components

**`DoctorRecommendation.jsx`**
- Displays AI-generated recommendations in chat
- Shows recommended doctors with ratings and experience
- Provides direct contact options
- Crisis hotline access for urgent cases

**Updated `MessageBubble.jsx`**
- Renders doctor recommendations after bot messages
- Passes session context for personalized recommendations

### Services

**`doctor.service.js`**
- API client for all doctor-related operations
- Handles dashboard, appointments, patients, prescriptions
- Search and recommendation retrieval

## Setup Instructions

### 1. Database Setup

```bash
cd mental_health_chatbot/backend

# Create tables (automatic on startup)
python main.py

# Seed sample doctors
python seed_doctors.py
```

### 2. Backend Configuration

The doctor system is automatically integrated when you start the backend:

```bash
cd mental_health_chatbot/backend
python main.py
```

### 3. Frontend Configuration

Update `react_web/src/services/api.service.js` to ensure it points to your backend:

```javascript
const API_BASE_URL = 'http://localhost:8000'
```

### 4. Test the Integration

1. Start a chat conversation
2. Mention symptoms like "I feel anxious" or "I can't sleep"
3. After 3-4 turns, the AI may recommend professional help
4. Click "Find a Doctor" to see available specialists

## How Recommendations Work

### Trigger Conditions

Recommendations are generated when:
1. **Crisis detected**: Immediate recommendation with urgent priority
2. **Symptom threshold**: 3+ concerning keywords detected
3. **Persistent negative emotions**: Multiple turns with sadness/anxiety
4. **Turn threshold**: After 3+ conversation turns (prevents premature recommendations)

### Recommendation Flow

```
User Message → Emotion Analysis → Symptom Detection → 
Recommendation Service → Database Storage → 
Display in Chat (if appropriate)
```

### Example Scenarios

**Scenario 1: Anxiety**
```
User: "I've been feeling really anxious lately"
AI: [Analyzes emotion: anxiety, intent: emotional support]
    [Detects symptoms: anxiety, worried, stressed]
    [Generates recommendation: psychologist, urgency: normal]
    [Shows recommendation after response]
```

**Scenario 2: Crisis**
```
User: "I don't want to live anymore"
AI: [Crisis detected immediately]
    [Generates recommendation: psychiatrist, urgency: urgent]
    [Shows crisis resources + recommendation]
```

## Doctor Dashboard

Doctors can access their dashboard at `/doctor-dashboard` with:
- Today's appointments
- Pending requests
- Patient list
- Prescription history
- AI-powered workload summaries

## Customization

### Adding New Specializations

Edit `services/doctor_recommendation_service.py`:

```python
SYMPTOM_PATTERNS = {
    "your_specialization": [
        "keyword1", "keyword2", "keyword3"
    ],
    # ... existing patterns
}
```

### Adjusting Recommendation Threshold

```python
# In DoctorRecommendationService.__init__
self.recommendation_threshold = 3  # Change this value
```

### Customizing Urgency Levels

```python
URGENCY_EMOTIONS = {
    "urgent": ["your_urgent_emotions"],
    "high": ["your_high_priority_emotions"],
    # ... etc
}
```

## API Examples

### Get Recommendations for Session

```bash
curl http://localhost:8000/api/doctor/recommendations/session-123
```

### Search for Psychiatrists

```bash
curl "http://localhost:8000/api/doctor/search?specialization=psychiatrist"
```

### Get Doctor Dashboard

```bash
curl "http://localhost:8000/api/doctor/dashboard?doctor_id=doc-001"
```

## Security Considerations

1. **Privacy**: Recommendations don't store message content, only metadata
2. **Crisis Events**: Logged separately for safety monitoring
3. **Authentication**: Add auth middleware for production use
4. **HIPAA Compliance**: Implement encryption and access controls for production

## Future Enhancements

- [ ] Real-time appointment booking
- [ ] Video consultation integration
- [ ] Insurance verification
- [ ] Prescription e-prescribing
- [ ] Patient portal for medical records
- [ ] Multi-language support for doctor profiles
- [ ] Rating and review system
- [ ] Automated follow-up reminders

## Troubleshooting

**No recommendations appearing:**
- Check if backend is running
- Verify database tables created (`python seed_doctors.py`)
- Check browser console for API errors
- Ensure conversation has 3+ turns

**Doctors not loading:**
- Run seed script: `python seed_doctors.py`
- Check API endpoint: `GET /api/doctor/search`
- Verify database connection

**Dashboard not working:**
- Ensure doctor_id is valid
- Check if appointments/patients exist
- Verify API routes are registered in `main.py`

## Support

For issues or questions:
1. Check backend logs for errors
2. Verify API responses in browser DevTools
3. Review database tables for data integrity
4. Check this guide for configuration steps
