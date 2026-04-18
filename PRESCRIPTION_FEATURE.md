# Prescription Analyzer & Reminder System

## Overview
This feature allows users to upload prescription images, extract medicine information using OCR, and create automated reminder schedules.

## Features

### 1. Prescription Upload & Analysis
- Upload prescription images (JPG, PNG, max 10MB)
- OCR text extraction from prescription images
- AI-powered medicine extraction with:
  - Medicine name
  - Dosage
  - Frequency
  - Instructions
  - Suggested reminder times

### 2. Reminder Schedule Creation
- Review extracted medicines
- Customize reminder times for each medicine
- Add multiple reminder times per medicine
- Automatic schedule creation

### 3. Medicine Reminder Page
- View all active medicine reminders
- Track daily doses (doses taken / doses per day)
- Visual progress indicators
- Increment/decrement dose counters
- Real-time sync with backend

## Architecture

### Backend (FastAPI)
- **Location**: `mental_health_chatbot/backend/`
- **Routes**: `api/prescription_routes.py`
- **Database Models**: `database/models.py`
  - `PrescriptionAnalysis` - Stores uploaded prescriptions
  - `MedicineReminder` - Stores reminder schedules
- **Database Functions**: `database/db.py`

### Frontend (React)
- **Location**: `react_web/src/`
- **Components**:
  - `components/chat/PrescriptionModal.jsx` - Upload & analysis modal
  - `components/chat/PrescriptionModal.css` - Modal styles
- **Pages**:
  - `pages/MedicineReminderPage.jsx` - Reminder dashboard

## API Endpoints

### POST `/api/prescription/upload`
Upload and analyze prescription image
- **Body**: FormData with `file` and `session_id`
- **Response**: Extracted medicines with analysis

### GET `/api/prescription/list/{session_id}`
Get all prescriptions for a session

### POST `/api/prescription/schedule`
Create reminder schedule from prescription
- **Body**: `{ prescription_id, medicines[] }`

### GET `/api/prescription/reminders/{session_id}`
Get all reminders for a session

### PATCH `/api/prescription/reminders/dose`
Update dose taken count
- **Body**: `{ reminder_id, doses_taken }`

### DELETE `/api/prescription/reminders/{reminder_id}`
Delete a reminder

## Usage

### 1. Start Backend
```bash
cd mental_health_chatbot/backend
python main.py
```

### 2. Start Frontend
```bash
cd react_web
npm run dev
```

### 3. Upload Prescription
1. Open chat interface
2. Click the pill icon (💊) button
3. Upload prescription image
4. Review extracted medicines
5. Customize reminder times
6. Create schedule

### 4. View Reminders
1. Navigate to Medicine Reminder page
2. View all active reminders
3. Track daily doses
4. Update dose counts

## Integration Points

### Chat Input
- Added prescription button (Pill icon)
- Opens PrescriptionModal on click
- Passes session ID to modal

### Medicine Reminder Page
- Fetches reminders from backend
- Real-time dose tracking
- Syncs with backend on updates

## Future Enhancements

### OCR Integration
Currently using mock data. To integrate real OCR:
1. Install RapidOCR: `pip install rapidocr-onnxruntime`
2. Update `extract_text_from_image()` in `prescription_routes.py`

### LLM Integration
Currently using mock extraction. To integrate real LLM:
1. Use existing LLM service from mental health chatbot
2. Update `analyze_prescription_text()` in `prescription_routes.py`
3. Add structured output parsing

### Notifications
- Browser notifications for medicine reminders
- Email/SMS reminders
- Push notifications

### Analytics
- Adherence tracking
- Missed dose alerts
- Weekly/monthly reports

## Database Schema

### prescription_analyses
```sql
id: String (UUID)
session_id: String
filename: String
extracted_text: Text
medicines: Text (JSON)
notes: Text
created_at: DateTime
```

### medicine_reminders
```sql
id: String (UUID)
session_id: String
prescription_id: String
medicine_name: String
dosage: String
time: String (HH:MM)
instructions: Text
doses_per_day: Integer
doses_taken: Integer
created_at: DateTime
```

## Testing

### Test Prescription Upload
```bash
curl -X POST http://localhost:8000/api/prescription/upload \
  -F "file=@prescription.jpg" \
  -F "session_id=test-session"
```

### Test Get Reminders
```bash
curl http://localhost:8000/api/prescription/reminders/test-session
```

## Notes
- Session ID is stored in localStorage
- Default session ID: 'default-session'
- Images are validated for type and size
- All times are in 24-hour format (HH:MM)
