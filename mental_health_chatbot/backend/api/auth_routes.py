"""Authentication routes"""
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import jwt
import hashlib

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # TODO: Move to env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


# Helper functions - Simple SHA256 hashing (for demo purposes)
def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password


# In-memory user storage (replace with database later)
users_db = {}

# Seed doctors on module load (only once)
_seeded = False

def seed_initial_doctors():
    """Seed initial doctor accounts"""
    global _seeded
    if _seeded:
        return
    
    doctors = [
        {
            "id": "doc-001",
            "name": "Dr. Sarah Johnson",
            "email": "sarah.johnson@mediscan.com",
            "password": hash_password("doctor123"),
            "role": "doctor",
            "specialization": "psychiatrist",
            "experience_years": 15,
            "bio": "Board-certified psychiatrist with 15 years of experience in treating depression, anxiety, and mood disorders.",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "doc-002",
            "name": "Dr. Michael Chen",
            "email": "michael.chen@mediscan.com",
            "password": hash_password("doctor123"),
            "role": "doctor",
            "specialization": "psychologist",
            "experience_years": 12,
            "bio": "Clinical psychologist specializing in anxiety disorders, trauma, and PTSD.",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "doc-003",
            "name": "Dr. Emily Rodriguez",
            "email": "emily.rodriguez@mediscan.com",
            "password": hash_password("doctor123"),
            "role": "doctor",
            "specialization": "therapist",
            "experience_years": 8,
            "bio": "Licensed marriage and family therapist with expertise in relationship counseling.",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "doc-004",
            "name": "Dr. Rajesh Kumar",
            "email": "rajesh.kumar@mediscan.com",
            "password": hash_password("doctor123"),
            "role": "doctor",
            "specialization": "psychiatrist",
            "experience_years": 20,
            "bio": "Senior psychiatrist specializing in severe mental health conditions and medication management.",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": "doc-005",
            "name": "Dr. Priya Sharma",
            "email": "priya.sharma@mediscan.com",
            "password": hash_password("doctor123"),
            "role": "doctor",
            "specialization": "psychologist",
            "experience_years": 10,
            "bio": "Child and adolescent psychologist with focus on anxiety and behavioral issues.",
            "created_at": datetime.utcnow().isoformat(),
        }
    ]
    
    for doctor in doctors:
        users_db[doctor["id"]] = doctor
    
    _seeded = True
    logger.info(f"✅ Seeded {len(doctors)} doctor accounts")

# Seed doctors immediately
seed_initial_doctors()


# Schemas
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "patient"  # patient or doctor


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id or user_id not in users_db:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return users_db[user_id]


# Routes
@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Register a new user"""
    try:
        # Check if user already exists
        if any(u["email"] == request.email for u in users_db.values()):
            logger.warning(f"⚠️ Registration attempt with existing email: {request.email}")
            raise HTTPException(status_code=400, detail=f"Email {request.email} is already registered. Please login instead.")
        
        # Validate role
        if request.role not in ["patient", "doctor"]:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'patient' or 'doctor'")
        
        # Create user
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": request.name,
            "email": request.email,
            "password": hash_password(request.password),
            "role": request.role,
            "created_at": datetime.utcnow().isoformat(),
        }
        users_db[user_id] = user
        
        logger.info(f"✅ User registered: {request.email} (role: {request.role})")
        
        # Create access token
        access_token = create_access_token(data={"sub": user_id})
        
        # Return response
        return AuthResponse(
            access_token=access_token,
            user=UserResponse(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                role=user["role"],
                created_at=user["created_at"],
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during registration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login user"""
    try:
        # Find user by email
        user = next((u for u in users_db.values() if u["email"] == request.email), None)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not verify_password(request.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        logger.info(f"✅ User logged in: {request.email} (role: {user['role']})")
        
        # Create access token
        access_token = create_access_token(data={"sub": user["id"]})
        
        # Return response
        return AuthResponse(
            access_token=access_token,
            user=UserResponse(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                role=user["role"],
                created_at=user["created_at"],
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
        created_at=current_user["created_at"],
    )


@router.post("/google")
async def google_login():
    """Google OAuth login (placeholder)"""
    raise HTTPException(status_code=501, detail="Google login not implemented yet")
