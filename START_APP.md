# 🚀 Quick Start - No Login Required!

## Start the App (2 Steps)

### Step 1: Start Backend

Open **Terminal 1** (PowerShell):

```powershell
cd D:\p_hack\py_server
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: `http://localhost:8000`

---

### Step 2: Start Frontend

Open **Terminal 2** (PowerShell):

```powershell
cd D:\p_hack\react_web
npm run dev
```

✅ Frontend running at: `http://localhost:5173`

---

## Access the App

Open your browser and go to:

```
http://localhost:5173
```

**You'll see the diagnosis page immediately - NO LOGIN REQUIRED!** 🎉

---

## Test the System

1. **Upload an image** (any image works for testing)
2. **Select symptoms**: Click on symptoms like "itching", "redness"
3. **Click "Analyze"** button
4. **See results** in < 3 seconds!

---

## What You'll See

The diagnosis page shows:
- 📷 Image upload area
- ✅ Symptom selection buttons
- 🔍 Analyze button
- 📊 Results with:
  - Disease prediction
  - Confidence percentage
  - Risk level (color-coded)
  - Detailed explanation
  - All disease probabilities

---

## Troubleshooting

### Backend won't start?
```powershell
# Make sure you're in the right directory
cd D:\p_hack\py_server

# Activate virtual environment
.\venv\Scripts\activate

# Check if dependencies are installed
pip list

# If not, install them
pip install -r requirements.txt
```

### Frontend won't start?
```powershell
# Make sure you're in the right directory
cd D:\p_hack\react_web

# Check if node_modules exists
# If not, run:
npm install

# Then start
npm run dev
```

### Can't access the page?
- Check both terminals are running
- Backend should show: "Uvicorn running on http://0.0.0.0:8000"
- Frontend should show: "Local: http://localhost:5173"
- Open: `http://localhost:5173` in your browser

### MongoDB error in backend?
- **This is OK!** You can ignore it
- The diagnosis feature works without MongoDB
- MongoDB is only for user authentication (not needed)

---

## Stop the App

Press `Ctrl + C` in both terminal windows

---

## Quick Commands Reference

```powershell
# Backend
cd D:\p_hack\py_server
.\venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend (in new terminal)
cd D:\p_hack\react_web
npm run dev

# Access
# Open browser: http://localhost:5173
```

---

## Demo Ready! 🏆

Your app is now running and ready for:
- ✅ Testing
- ✅ Demo
- ✅ Hackathon presentation
- ✅ Real-world use

**No login required - just open and use!** 🚀
