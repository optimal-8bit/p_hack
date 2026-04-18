# Install Authentication Backend

## Issue
You're getting "not found" errors when signing up because the authentication backend doesn't exist yet.

## Solution
Install the auth dependencies and restart the backend.

## Steps:

### 1. Install New Dependencies

```bash
cd p_hack/mental_health_chatbot
source backend/venv/bin/activate
pip install pyjwt==2.8.0 passlib[bcrypt]==1.7.4 python-jose[cryptography]==3.3.0
```

### 2. Restart Backend

```bash
# Stop the current backend (Ctrl+C)
# Then restart:
python backend/main.py
```

### 3. Test Registration

1. Go to your frontend: `http://localhost:5173`
2. Click "SIGN UP"
3. Fill in the form:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: Patient or Doctor
4. Click "Create account"
5. Should redirect to chat (patient) or doctor dashboard (doctor)

## What Was Added

### Backend Files:
- `backend/api/auth_routes.py` - Authentication endpoints
  - POST `/auth/register` - Register new user
  - POST `/auth/login` - Login user
  - GET `/auth/me` - Get current user profile

### Features:
- ✅ User registration with role (patient/doctor)
- ✅ User login with email/password
- ✅ JWT token authentication
- ✅ Password hashing (bcrypt)
- ✅ Role-based routing
- ✅ In-memory user storage (will add database later)

### Security:
- Passwords are hashed with bcrypt
- JWT tokens expire after 7 days
- Token validation on protected routes

## Current Limitations

⚠️ **In-Memory Storage**: Users are stored in memory, so they're lost when backend restarts. This is temporary - we'll add database persistence later.

## After Installation

You should see in backend logs:
```
✅ User registered: test@example.com (role: patient)
```

And in frontend:
- Patient → Redirects to `/chat`
- Doctor → Redirects to `/doctor/dashboard`

## Next Steps (Optional)

1. Add database persistence for users
2. Connect patient registration to `patients` table
3. Connect doctor registration to `doctors` table
4. Add email verification
5. Add password reset

---

**Run the install commands above and restart your backend!**
