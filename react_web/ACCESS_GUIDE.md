# 🔐 Access Guide

## Quick Access (No Login Required) ✅

The diagnosis page is now **publicly accessible** - no login needed!

### Access the App:

1. **Start the backend:**
   ```bash
   cd py_server
   uvicorn app.main:app --reload
   ```

2. **Start the frontend:**
   ```bash
   cd react_web
   npm run dev
   ```

3. **Open in browser:**
   ```
   http://localhost:5173
   ```

4. **You'll be automatically redirected to:**
   ```
   http://localhost:5173/diagnosis
   ```

**That's it! No login required!** 🎉

---

## If You Want to Use Login (Optional)

### Option 1: Register a New Account

1. Go to: `http://localhost:5173/register`
2. Fill in:
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Register"
4. You'll be logged in automatically

### Option 2: Login with Existing Account

1. Go to: `http://localhost:5173/login`
2. Enter credentials:
   - Email: Your registered email
   - Password: Your password
3. Click "Sign in"

### Option 3: Google Sign-In (Requires Setup)

To enable Google sign-in:

1. Get Google OAuth Client ID from [Google Cloud Console](https://console.cloud.google.com/)
2. Create `.env` file in `react_web/`:
   ```
   VITE_API_BASE_URL=http://localhost:8000/api/v1
   VITE_GOOGLE_CLIENT_ID=your-google-client-id-here
   ```
3. Restart the dev server
4. Click "Continue with Google" on login page

---

## Backend Setup for Authentication

The backend needs MongoDB for user authentication:

### Start MongoDB (if you want to use auth):

**Option 1: Local MongoDB**
```bash
# Install MongoDB from https://www.mongodb.com/try/download/community
# Start MongoDB service
mongod
```

**Option 2: MongoDB Atlas (Cloud)**
1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Get connection string
3. Update `.env` in `py_server/`:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   ```

**Option 3: Skip MongoDB (Diagnosis works without it)**
- The diagnosis feature uses SQLite
- MongoDB is only for user authentication
- You can use the app without MongoDB if diagnosis page is public

---

## Current Setup (Recommended for Demo)

✅ **Diagnosis page is PUBLIC**
- No login required
- No MongoDB required
- Works immediately
- Perfect for hackathon demo

### Access Flow:
```
Open browser → http://localhost:5173 → Diagnosis Page (instant access)
```

---

## Routes Available:

| Route | Access | Purpose |
|-------|--------|---------|
| `/` | Public | Redirects to `/diagnosis` |
| `/diagnosis` | **Public** ✅ | AI diagnosis tool |
| `/login` | Public | Login page |
| `/register` | Public | Registration page |
| `/dashboard` | Protected 🔒 | Requires login |

---

## Troubleshooting

### "Cannot connect to backend"
- Ensure backend is running: `uvicorn app.main:app --reload`
- Check backend URL in `.env`: `VITE_API_BASE_URL=http://localhost:8000/api/v1`

### "MongoDB connection error"
- This is OK! Diagnosis works without MongoDB
- MongoDB is only needed for user authentication
- The diagnosis feature uses SQLite (no setup needed)

### "Page not found"
- Make sure frontend is running: `npm run dev`
- Navigate to: `http://localhost:5173`

---

## For Production Deployment

### Make Diagnosis Public (Recommended):
- Already configured! ✅
- No authentication required
- Perfect for rural clinics

### Require Authentication (Optional):
- Uncomment `<ProtectedRoute>` in `AppRouter.jsx`
- Setup MongoDB
- Configure environment variables

---

## Quick Test

1. Open: `http://localhost:5173`
2. You should see the diagnosis page immediately
3. Upload an image or select symptoms
4. Click "Analyze"
5. Get results in < 3 seconds!

**No login needed!** 🚀
