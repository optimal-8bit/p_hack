# 🚀 Quick Start Guide

Get the Offline AI Health Assistant running in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed
- Terminal/Command Prompt

## Step 1: Start Backend (2 minutes)

```bash
# Navigate to backend
cd py_server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: http://localhost:8000

## Step 2: Start Frontend (2 minutes)

Open a NEW terminal:

```bash
# Navigate to frontend
cd react_web

# Install dependencies
npm install

# Create environment file
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env

# Start development server
npm run dev
```

✅ Frontend running at: http://localhost:5173

## Step 3: Test the System (1 minute)

1. Open browser: http://localhost:5173
2. Login or register (if auth is enabled)
3. Navigate to diagnosis page
4. Upload a test image (any image works)
5. Select symptoms: itching, redness
6. Click "Analyze"
7. See results in < 3 seconds!

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
# Update frontend .env: VITE_API_BASE_URL=http://localhost:8001/api/v1
```

**MongoDB connection error:**
- The system works without MongoDB
- MongoDB is only for auth/users (optional)
- Diagnosis uses SQLite (no setup needed)

### Frontend Issues

**Port 5173 already in use:**
```bash
# Vite will automatically use next available port
# Check terminal output for actual port
```

**API connection error:**
- Ensure backend is running
- Check .env file has correct API URL
- Verify no firewall blocking localhost

## Testing Without Images

You can test with symptoms only:
1. Don't upload image
2. Select symptoms
3. Click Analyze
4. System uses symptom-based analysis

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [API Endpoints](#) section for integration
- Review code architecture in backend modules
- Customize diseases and symptoms as needed

## Production Deployment

### Quick Deploy to Render (Backend)
```bash
cd py_server
git init
git add .
git commit -m "Initial commit"
# Push to GitHub and connect to Render
```

### Quick Deploy to Vercel (Frontend)
```bash
cd react_web
npm install -g vercel
vercel --prod
# Set environment variable: VITE_API_BASE_URL
```

## Offline Clinic Setup

For use without internet:

1. **Setup server machine:**
   ```bash
   # Get server's local IP
   # Windows: ipconfig
   # Mac/Linux: ifconfig
   
   # Start backend with 0.0.0.0
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Configure client devices:**
   ```bash
   # Update .env with server IP
   VITE_API_BASE_URL=http://192.168.1.100:8000/api/v1
   
   # Build frontend
   npm run build
   
   # Serve from any device on network
   ```

3. **Access from tablets/phones:**
   - Connect to same WiFi/LAN
   - Open browser to frontend URL
   - No internet required!

## Support

Having issues? Check:
1. Python version: `python --version` (need 3.10+)
2. Node version: `node --version` (need 18+)
3. Backend logs in terminal
4. Browser console (F12) for frontend errors
5. Ensure both servers are running

---

**You're ready to go! 🎉**

The system is now running offline and ready to diagnose patients.
