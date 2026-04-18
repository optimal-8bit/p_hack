# Quick Start - Prescription Feature

## 🚀 5-Minute Setup

### Step 1: Verify Backend is Running (30 seconds)

```bash
# Test if backend is accessible
python test_prescription_simple.py
```

**Expected output:**
```
✓ Status: 200
✓ Found 0 reminders
```

If you see this, backend is working! ✅

### Step 2: Open Frontend (10 seconds)

Open your browser to: **http://localhost:5173**

### Step 3: Test Upload (2 minutes)

1. Click the **pill icon (💊)** in the chat input
2. Upload **any image** (JPG or PNG)
3. Click **"Analyze Prescription"**
4. You'll see 3 mock medicines extracted
5. Click **"Create Reminder Schedule"**
6. Success! ✅

### Step 4: View Reminders (1 minute)

1. Click **"Medicine Reminder"** button (top-right)
2. You should see your 3 medicines with reminders
3. Try clicking **+** and **−** buttons to track doses

### Step 5: Verify in Console (1 minute)

Press **F12** to open DevTools, then check:

**Console Tab:**
```
✓ Upload successful
✓ Schedule created successfully
✓ Fetched reminders: [...]
```

**Network Tab:**
```
✓ POST /api/prescription/upload → 200
✓ POST /api/prescription/schedule → 200
✓ GET /api/prescription/reminders/... → 200
```

## ✅ Success Checklist

- [ ] Backend test script shows ✓ Status: 200
- [ ] Pill icon (💊) visible in chat input
- [ ] Modal opens when clicking pill icon
- [ ] Image uploads successfully
- [ ] 3 medicines appear in review step
- [ ] Schedule creates successfully
- [ ] Reminders appear on reminder page
- [ ] Dose counters work (+/− buttons)
- [ ] Browser console shows successful API calls
- [ ] No errors in backend terminal

## 🐛 Quick Troubleshooting

### Problem: "Backend test fails"
**Solution:** Start backend:
```bash
cd mental_health_chatbot/backend
python main.py
```

### Problem: "Pill icon not visible"
**Solution:** 
1. Hard refresh: Ctrl+Shift+R
2. Check you're on the chat page
3. Look between + button and text input

### Problem: "No reminders appear"
**Solution:**
1. Open browser console (F12)
2. Check for errors
3. Verify session ID: `localStorage.getItem('sessionId')`
4. Check Network tab for API calls
5. See `PRESCRIPTION_TROUBLESHOOTING.md`

### Problem: "Upload fails"
**Solution:**
1. Check file is image (JPG/PNG)
2. Check file size < 10MB
3. Check browser console for error
4. Check backend logs

## 📝 What You're Testing

### Mock Data (Currently Active)
- **OCR:** Returns sample prescription text
- **Extraction:** Returns 3 sample medicines:
  - Aspirin 100mg (2x daily)
  - Vitamin D 1000 IU (1x daily)
  - Metformin 500mg (3x daily)

### Real Flow (Working)
1. Upload image → Backend receives file
2. Extract text → Mock OCR (ready for real OCR)
3. Analyze → Mock extraction (ready for real LLM)
4. Save → Database stores prescription
5. Create schedule → Database stores reminders
6. View reminders → Fetches from database
7. Track doses → Updates database

## 🎯 Expected Behavior

### After Upload:
- Modal shows "Extracted Medicines" section
- 3 medicine cards appear
- Each has name, dosage, instructions
- Each has customizable reminder times
- Can add/remove times with buttons

### After Schedule Creation:
- Success message appears
- Modal closes
- Can navigate to reminder page

### On Reminder Page:
- 6 reminder cards appear (2+1+3 from the 3 medicines)
- Each shows medicine name, dosage, time
- Each has dose counter (0/X)
- Each has progress bar
- +/− buttons work
- Changes save to backend

## 💡 Pro Tips

1. **Check Console First:** Most issues show up in browser console
2. **Use Same Session:** Don't clear localStorage during testing
3. **Backend Logs:** Watch backend terminal for detailed logs
4. **Network Tab:** Shows exact API requests/responses
5. **Test Script:** Run `python test_prescription_simple.py` to verify API

## 🎉 Success!

If you can:
- ✅ Upload an image
- ✅ See extracted medicines
- ✅ Create a schedule
- ✅ View reminders on reminder page
- ✅ Update dose counters

**Then everything is working perfectly!** 🎊

## 📚 More Help

- **Detailed debugging:** See `PRESCRIPTION_TROUBLESHOOTING.md`
- **Feature overview:** See `PRESCRIPTION_FEATURE.md`
- **Setup guide:** See `setup_prescription_feature.md`
- **User guide:** See `PRESCRIPTION_FEATURE_GUIDE.md`

## 🔄 Reset & Retry

If something goes wrong, reset everything:

```bash
# 1. Stop backend (Ctrl+C)

# 2. Delete database
rm mental_health_chatbot/backend/chat_history.db

# 3. Clear browser storage (in browser console)
localStorage.clear()

# 4. Restart backend
cd mental_health_chatbot/backend
python main.py

# 5. Hard refresh frontend
# Press: Ctrl+Shift+R

# 6. Try again!
```

## ⏱️ Time Estimate

- First time setup: **5 minutes**
- Subsequent tests: **1 minute**
- Full flow test: **2 minutes**

## 🎬 Video Walkthrough (Text Version)

```
00:00 - Open http://localhost:5173
00:05 - Click pill icon (💊) in chat input
00:10 - Modal opens with upload area
00:15 - Click upload area, select any image
00:20 - Image preview appears
00:25 - Click "Analyze Prescription"
00:30 - Loading... (backend processing)
00:35 - 3 medicines appear in review
00:40 - Scroll through medicines
00:45 - Customize times if desired
00:50 - Click "Create Reminder Schedule"
00:55 - Success message appears
01:00 - Click "Done"
01:05 - Click "Medicine Reminder" button
01:10 - Reminder page loads
01:15 - 6 reminder cards appear
01:20 - Click + button on first card
01:25 - Counter updates: 0/2 → 1/2
01:30 - Progress bar animates
01:35 - Test complete! ✅
```

---

**Ready? Let's test!** 🚀

Run: `python test_prescription_simple.py`

Then open: http://localhost:5173

Click the pill icon and follow the steps above!
