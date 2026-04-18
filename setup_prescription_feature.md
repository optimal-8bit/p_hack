# Setup Prescription Feature

## Quick Start Guide

### 1. Backend Setup

```bash
# Navigate to backend
cd mental_health_chatbot/backend

# Install Python dependencies (if not already installed)
pip install fastapi uvicorn sqlalchemy aiosqlite python-multipart

# Optional: Install RapidOCR for real OCR (currently using mock data)
# pip install rapidocr-onnxruntime pillow numpy

# Run backend
python main.py
```

Backend will start at: http://localhost:8000

### 2. Frontend Setup

```bash
# Navigate to frontend
cd react_web

# Install dependencies (if not already installed)
npm install

# Run frontend
npm run dev
```

Frontend will start at: http://localhost:5173

### 3. Test the Feature

1. Open browser: http://localhost:5173
2. Login/Register
3. Go to chat page
4. Click the pill icon (💊) in the chat input
5. Upload a prescription image
6. Review extracted medicines
7. Set reminder times
8. Create schedule
9. Navigate to "Medicine Reminder" page to view reminders

## File Structure

```
mental_health_chatbot/backend/
├── api/
│   ├── routes.py                    # Existing chat routes
│   └── prescription_routes.py       # NEW: Prescription routes
├── database/
│   ├── models.py                    # Updated with new models
│   └── db.py                        # Updated with new functions
└── main.py                          # Updated to include prescription routes

react_web/src/
├── components/
│   └── chat/
│       ├── ChatInput.jsx            # Updated with prescription button
│       ├── PrescriptionModal.jsx    # NEW: Prescription modal
│       └── PrescriptionModal.css    # NEW: Modal styles
├── pages/
│   └── MedicineReminderPage.jsx     # Updated to fetch from backend
└── styles/
    └── MentalHealthChat.css         # Updated with prescription button styles
```

## Database Migration

The new tables will be created automatically on first run:
- `prescription_analyses` - Stores uploaded prescriptions
- `medicine_reminders` - Stores reminder schedules

No manual migration needed!

## API Testing

### Test Health Check
```bash
curl http://localhost:8000/api/health
```

### Test Prescription Upload (with mock image)
```bash
# Create a test image first
curl -X POST http://localhost:8000/api/prescription/upload \
  -F "file=@test_prescription.jpg" \
  -F "session_id=test-123"
```

### Test Get Reminders
```bash
curl http://localhost:8000/api/prescription/reminders/test-123
```

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in mental_health_chatbot/backend/config.py
PORT = 8001  # Change from 8000
```

**Database errors:**
```bash
# Delete and recreate database
rm mental_health_chatbot/backend/chat_history.db
python mental_health_chatbot/backend/main.py
```

### Frontend Issues

**CORS errors:**
- Backend already has CORS enabled for all origins
- Check if backend is running on port 8000

**API connection errors:**
- Verify backend is running: http://localhost:8000/api/health
- Check browser console for errors

**Modal not opening:**
- Check browser console for errors
- Verify PrescriptionModal is imported in ChatInput.jsx

## Next Steps

### Enable Real OCR
1. Install RapidOCR:
   ```bash
   pip install rapidocr-onnxruntime pillow numpy
   ```

2. Update `prescription_routes.py`:
   ```python
   from rapidocr_onnxruntime import RapidOCR
   from PIL import Image
   import numpy as np
   from io import BytesIO
   
   async def extract_text_from_image(image_bytes: bytes) -> str:
       image = Image.open(BytesIO(image_bytes)).convert("RGB")
       image_array = np.array(image)
       engine = RapidOCR()
       result, _ = engine(image_array)
       
       if not result:
           return ""
       
       lines = [item[1] for item in result if len(item) >= 2]
       return "\n".join(lines).strip()
   ```

### Enable Real LLM Extraction
Use the existing LLM service from the mental health chatbot:
```python
from pipeline.orchestrator import get_orchestrator

async def analyze_prescription_text(text: str) -> List[MedicineItem]:
    # Use your existing LLM service here
    # Parse structured output into MedicineItem objects
    pass
```

## Features Working

✅ Prescription upload modal in chat
✅ Image preview and validation
✅ Mock OCR text extraction
✅ Mock medicine extraction
✅ Reminder time customization
✅ Schedule creation
✅ Medicine reminder page
✅ Dose tracking
✅ Real-time backend sync
✅ Database persistence

## Features Pending (Optional)

⏳ Real OCR integration (RapidOCR)
⏳ Real LLM extraction
⏳ Browser notifications
⏳ Email/SMS reminders
⏳ Adherence analytics
⏳ Export schedules

## Support

For issues or questions:
1. Check browser console for errors
2. Check backend logs
3. Verify all files are in correct locations
4. Ensure both frontend and backend are running
