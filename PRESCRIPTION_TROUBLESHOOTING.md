# Prescription Feature - Troubleshooting Guide

## ✅ Backend is Working

The API endpoints are confirmed working:
- ✓ Health check: `http://localhost:8000/api/health`
- ✓ Get reminders: `http://localhost:8000/api/prescription/reminders/{session_id}`
- ✓ Upload endpoint: `http://localhost:8000/api/prescription/upload`
- ✓ Schedule endpoint: `http://localhost:8000/api/prescription/schedule`

## 🔍 Debugging Steps

### Step 1: Check Browser Console

Open browser DevTools (F12) and check the Console tab for logs:

**Expected logs when uploading:**
```
Uploading prescription... {sessionId: "session-...", fileName: "..."}
Upload response status: 200
Upload successful: {prescription_id: "...", medicines: [...]}
Medicines set: [...]
```

**Expected logs when creating schedule:**
```
Creating schedule... {sessionId: "...", prescriptionId: "...", medicinesCount: 3}
Schedule response status: 200
Schedule created successfully: {status: "success", message: "...", reminder_ids: [...]}
```

**Expected logs on reminder page:**
```
Fetching reminders for session: session-...
Reminders response status: 200
Fetched reminders: [...]
```

### Step 2: Check Network Tab

Open browser DevTools → Network tab:

1. **Upload Request:**
   - URL: `http://localhost:8000/api/prescription/upload`
   - Method: POST
   - Status: 200
   - Response should contain `prescription_id` and `medicines` array

2. **Schedule Request:**
   - URL: `http://localhost:8000/api/prescription/schedule?session_id=...`
   - Method: POST
   - Status: 200
   - Response should contain `reminder_ids` array

3. **Get Reminders Request:**
   - URL: `http://localhost:8000/api/prescription/reminders/{session_id}`
   - Method: GET
   - Status: 200
   - Response should be array of reminders

### Step 3: Check Session ID

The session ID must be consistent across all requests:

1. Open browser console
2. Type: `localStorage.getItem('sessionId')`
3. Note the session ID
4. Verify it's being used in all API calls

### Step 4: Verify Backend Logs

Check the backend terminal for logs:

**Expected logs:**
```
INFO: Received prescription upload for session: session-...
INFO: File size: ... bytes, type: image/...
INFO: Extracted text length: ...
INFO: Extracted 3 medicines
INFO: Saved prescription analysis with ID: ...
INFO: Created reminder ... for Aspirin at 09:00
INFO: Created reminder ... for Vitamin D at 08:00
INFO: Created 6 reminders for session session-...
```

## 🐛 Common Issues & Solutions

### Issue 1: "No reminders found" on reminder page

**Cause:** Reminders not created or wrong session ID

**Solution:**
1. Check browser console for session ID
2. Verify schedule was created successfully (check console logs)
3. Try refreshing the reminder page
4. Check backend logs for errors

### Issue 2: Upload fails with error

**Cause:** File validation or backend error

**Solution:**
1. Check file is an image (JPG, PNG)
2. Check file size < 10MB
3. Check backend is running
4. Check browser console for error details
5. Check backend logs for stack trace

### Issue 3: Schedule creation fails

**Cause:** Missing prescription_id or invalid data

**Solution:**
1. Check browser console for the request payload
2. Verify `prescription_id` is present
3. Verify `medicines` array has correct structure
4. Check backend logs for validation errors

### Issue 4: Reminders not persisting

**Cause:** Database not saving or session ID mismatch

**Solution:**
1. Check database file exists: `mental_health_chatbot/backend/chat_history.db`
2. Verify session ID is consistent
3. Check backend logs for database errors
4. Try deleting database and restarting backend

## 🧪 Manual Testing

### Test 1: Upload Prescription

```bash
# Create a test image (any image file)
# Then upload via curl:

curl -X POST http://localhost:8000/api/prescription/upload \
  -F "file=@test_image.jpg" \
  -F "session_id=manual-test-123"
```

**Expected response:**
```json
{
  "prescription_id": "...",
  "extracted_text": "...",
  "medicines": [
    {
      "medicine_name": "Aspirin",
      "dosage": "100mg",
      "frequency": "Twice daily",
      "instructions": "Take 1 tablet after meals",
      "timings": ["09:00", "21:00"]
    }
  ],
  "notes": "...",
  "created_at": "..."
}
```

### Test 2: Create Schedule

```bash
curl -X POST "http://localhost:8000/api/prescription/schedule?session_id=manual-test-123" \
  -H "Content-Type: application/json" \
  -d '{
    "prescription_id": "YOUR_PRESCRIPTION_ID",
    "medicines": [
      {
        "medicine_name": "Aspirin",
        "dosage": "100mg",
        "instructions": "Take after meals",
        "timings": ["09:00", "21:00"]
      }
    ]
  }'
```

**Expected response:**
```json
{
  "status": "success",
  "message": "Created 2 reminders",
  "reminder_ids": ["...", "..."]
}
```

### Test 3: Get Reminders

```bash
curl http://localhost:8000/api/prescription/reminders/manual-test-123
```

**Expected response:**
```json
[
  {
    "id": "...",
    "medicine_name": "Aspirin",
    "dosage": "100mg",
    "time": "09:00",
    "instructions": "Take after meals",
    "doses_per_day": 2,
    "doses_taken": 0,
    "created_at": "..."
  }
]
```

## 📊 Data Flow Verification

### Complete Flow:

1. **User uploads image** → Frontend sends FormData to `/api/prescription/upload`
2. **Backend processes** → Extracts text (mock) → Analyzes medicines (mock) → Saves to DB
3. **Backend returns** → `prescription_id` + `medicines` array
4. **User reviews** → Customizes reminder times
5. **User creates schedule** → Frontend sends medicines to `/api/prescription/schedule`
6. **Backend creates reminders** → One reminder per medicine per timing → Saves to DB
7. **Backend returns** → `reminder_ids` array
8. **User views reminders** → Frontend fetches from `/api/prescription/reminders/{session_id}`
9. **Backend returns** → Array of all reminders for that session

### Verify Each Step:

```javascript
// Step 1: Check upload response
console.log('Upload response:', uploadResponse)
// Should have: prescription_id, medicines

// Step 2: Check medicines structure
console.log('Medicines:', medicines)
// Each should have: medicine_name, dosage, instructions, timings

// Step 3: Check schedule request
console.log('Schedule request:', {
  prescription_id,
  medicines
})

// Step 4: Check schedule response
console.log('Schedule response:', scheduleResponse)
// Should have: status, message, reminder_ids

// Step 5: Check reminders fetch
console.log('Fetched reminders:', reminders)
// Should be array with: id, medicine_name, dosage, time, etc.
```

## 🔧 Reset Everything

If nothing works, reset completely:

```bash
# 1. Stop backend (Ctrl+C)

# 2. Delete database
rm mental_health_chatbot/backend/chat_history.db

# 3. Clear browser storage
# In browser console:
localStorage.clear()
sessionStorage.clear()

# 4. Restart backend
cd mental_health_chatbot/backend
python main.py

# 5. Refresh frontend
# Hard refresh: Ctrl+Shift+R

# 6. Try again
```

## 📝 Checklist

Before reporting an issue, verify:

- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 5173
- [ ] Browser console shows no CORS errors
- [ ] Session ID is consistent across requests
- [ ] Upload returns 200 status
- [ ] Schedule creation returns 200 status
- [ ] Get reminders returns 200 status
- [ ] Backend logs show no errors
- [ ] Database file exists
- [ ] Browser DevTools Network tab shows successful requests

## 🎯 Quick Test

Run this in browser console on the chat page:

```javascript
// Test the full flow
async function testPrescriptionFlow() {
  const sessionId = localStorage.getItem('sessionId') || 'test-' + Date.now()
  console.log('Session ID:', sessionId)
  
  // Test 1: Get reminders (should work even if empty)
  const response = await fetch(`http://localhost:8000/api/prescription/reminders/${sessionId}`)
  const reminders = await response.json()
  console.log('Current reminders:', reminders)
  
  if (response.ok) {
    console.log('✓ API is working!')
    console.log('✓ Found', reminders.length, 'reminders')
  } else {
    console.error('✗ API error:', response.status)
  }
}

testPrescriptionFlow()
```

## 💡 Tips

1. **Always check browser console first** - Most issues show up there
2. **Use consistent session ID** - Don't mix different sessions
3. **Check backend logs** - They show detailed error messages
4. **Test with curl first** - Isolates frontend vs backend issues
5. **Use mock data** - The system works with mock OCR/LLM data
6. **Refresh after changes** - Hard refresh (Ctrl+Shift+R) after code changes

## 🆘 Still Not Working?

If you've tried everything:

1. Share browser console logs
2. Share backend terminal logs
3. Share Network tab screenshots
4. Share the exact steps you're taking
5. Share any error messages

The system is confirmed working - if it's not working for you, there's likely a simple configuration issue we can fix!
