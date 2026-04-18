# Doctor Recommendation Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (React Frontend)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CHAT INTERFACE                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  User: "I feel anxious and can't sleep"                  │  │
│  │  Bot: "I understand you're feeling anxious..."           │  │
│  │                                                           │  │
│  │  ┌────────────────────────────────────────────────┐     │  │
│  │  │  🩺 Professional Support Recommended           │     │  │
│  │  │  Recommended: Psychologist                     │     │  │
│  │  │  [Find a Doctor] [Call Crisis Line]            │     │  │
│  │  └────────────────────────────────────────────────┘     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                        │
│                                                                 │
│  POST /api/chat                                                 │
│  ├─> Emotion Analysis                                           │
│  ├─> Intent Classification                                      │
│  ├─> Safety Check (Crisis Detection)                            │
│  └─> Doctor Recommendation Service                              │
│                                                                 │
│  GET /api/doctor/search?specialization=psychologist             │
│  GET /api/doctor/recommendations/{session_id}                   │
│  GET /api/doctor/dashboard?doctor_id=doc-001                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE (SQLite)                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Doctors    │  │  Patients    │  │ Appointments │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────────────────────┐           │
│  │Prescriptions │  │  Doctor Recommendations      │           │
│  └──────────────┘  └──────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Recommendation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER SENDS MESSAGE                           │
│              "I feel anxious and can't sleep"                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CHAT ORCHESTRATOR                             │
│  1. Safety Check (Crisis Detection)                             │
│  2. Emotion Classification → "anxiety"                          │
│  3. Intent Classification → "anxiety and panic"                 │
│  4. Generate Response                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            DOCTOR RECOMMENDATION SERVICE                        │
│                                                                 │
│  analyze_conversation()                                         │
│  ├─> Detect Symptoms                                            │
│  │   ✓ "anxious" → anxiety symptom                             │
│  │   ✓ "can't sleep" → sleep problem                           │
│  │                                                              │
│  ├─> Match Specialization                                       │
│  │   anxiety + sleep → "psychologist"                          │
│  │                                                              │
│  ├─> Determine Urgency                                          │
│  │   anxiety emotion → "normal" urgency                        │
│  │                                                              │
│  └─> Generate Reason                                            │
│      "You're experiencing significant anxiety..."               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SAVE TO DATABASE                               │
│                                                                 │
│  DoctorRecommendation:                                          │
│  ├─ session_id: "session-123"                                   │
│  ├─ specialization: "psychologist"                              │
│  ├─ urgency: "normal"                                           │
│  ├─ symptoms: ["anxious", "can't sleep"]                        │
│  └─ recommended_doctors: [doc-002, doc-005]                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RETURN TO FRONTEND                             │
│                                                                 │
│  ChatResponse:                                                  │
│  ├─ response_text: "I understand..."                            │
│  ├─ emotion: "anxiety"                                          │
│  └─ doctor_recommendation:                                      │
│      ├─ should_recommend: true                                  │
│      ├─ specialization: "psychologist"                          │
│      ├─ reason: "You're experiencing..."                        │
│      └─ urgency: "normal"                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DISPLAY IN CHAT                                │
│                                                                 │
│  1. Show bot response                                           │
│  2. Render DoctorRecommendation component                       │
│  3. User clicks "Find a Doctor"                                 │
│  4. Fetch doctors: GET /api/doctor/search                       │
│  5. Display doctor list with ratings                            │
└─────────────────────────────────────────────────────────────────┘
```

## Symptom Detection Logic

```
┌─────────────────────────────────────────────────────────────────┐
│                   SYMPTOM PATTERNS                              │
└─────────────────────────────────────────────────────────────────┘

Psychiatrist (Severe Cases)
├─ "suicidal", "suicide", "kill myself"
├─ "severe depression", "can't get out of bed"
├─ "hearing voices", "hallucination"
└─ "paranoid", "delusion"

Psychologist (Therapy Cases)
├─ "anxiety", "panic attack", "worried"
├─ "trauma", "ptsd", "abuse"
├─ "grief", "loss", "depression"
└─ "relationship problems", "anger"

Therapist (Counseling)
├─ "talk to someone", "need help"
├─ "counseling", "therapy"
├─ "emotional support", "coping"
└─ "struggling"

General Practitioner
├─ "sleep problems", "insomnia"
├─ "fatigue", "tired"
├─ "headache", "physical symptoms"
└─ "medication", "prescription"
```

## Urgency Determination

```
┌─────────────────────────────────────────────────────────────────┐
│                   URGENCY LEVELS                                │
└─────────────────────────────────────────────────────────────────┘

URGENT (Red Alert)
├─ Crisis detected: true
├─ Emotions: suicidal, severe_distress, panic
├─ Action: Immediate recommendation + Crisis hotline
└─ Example: "I want to end my life"

HIGH (Yellow Warning)
├─ Emotions: anxiety, fear, anger, sadness
├─ Multiple severe symptoms
├─ Action: Prompt recommendation
└─ Example: "I have panic attacks daily"

NORMAL (Blue Info)
├─ Emotions: worried, stressed, confused
├─ General mental health concerns
├─ Action: Standard recommendation
└─ Example: "I feel anxious sometimes"

LOW (Green)
├─ Emotions: neutral, calm
├─ Preventive care
├─ Action: Optional recommendation
└─ Example: "I want to improve my mental health"
```

## Doctor Dashboard Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   DOCTOR LOGS IN                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              GET /api/doctor/dashboard                          │
│                                                                 │
│  Query Database:                                                │
│  ├─ Count total appointments                                    │
│  ├─ Filter today's appointments                                 │
│  ├─ Filter pending appointments                                 │
│  ├─ Count prescriptions                                         │
│  └─ Generate AI summary                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DISPLAY DASHBOARD                             │
│                                                                 │
│  ┌────────────────────────────────────────────────┐            │
│  │  📊 Metrics                                    │            │
│  │  ├─ Total Appointments: 156                    │            │
│  │  ├─ Today's Appointments: 8                    │            │
│  │  ├─ Pending: 12                                │            │
│  │  └─ Prescriptions: 89                          │            │
│  └────────────────────────────────────────────────┘            │
│                                                                 │
│  ┌────────────────────────────────────────────────┐            │
│  │  🤖 AI Workload Summary                        │            │
│  │  "Your workload is moderate today..."          │            │
│  └────────────────────────────────────────────────┘            │
│                                                                 │
│  ┌────────────────────────────────────────────────┐            │
│  │  📅 Today's Appointments                       │            │
│  │  ├─ 9:00 AM - John Doe (Confirmed)             │            │
│  │  ├─ 10:30 AM - Jane Smith (Confirmed)          │            │
│  │  └─ 2:00 PM - Mike Johnson (Pending)           │            │
│  └────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Summary

```
User Message
    ↓
Emotion + Intent Analysis
    ↓
Symptom Detection
    ↓
Recommendation Generation
    ↓
Database Storage
    ↓
API Response
    ↓
UI Display
    ↓
User Action (Find Doctor)
    ↓
Doctor Search
    ↓
Display Results
```

## Key Components

1. **Frontend (React)**
   - Chat interface
   - Doctor recommendation card
   - Doctor search/list
   - Dashboard

2. **Backend (FastAPI)**
   - Chat orchestrator
   - Recommendation service
   - Doctor routes
   - Database operations

3. **Database (SQLite)**
   - Doctors
   - Patients
   - Appointments
   - Recommendations

4. **AI Components**
   - Emotion classifier
   - Intent classifier
   - Symptom detector
   - Urgency calculator
