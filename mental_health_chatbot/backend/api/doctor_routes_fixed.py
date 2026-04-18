"""Doctor-related API routes - FIXED VERSION"""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/doctor", tags=["doctor"])


# Simple schemas for testing
class DashboardMetrics(BaseModel):
    total_appointments: int = 0
    todays_appointments: int = 0
    pending_appointments: int = 0
    total_prescriptions: int = 0


class DashboardResponse(BaseModel):
    metrics: DashboardMetrics
    ai_workload_summary: str = "Dashboard is working"
    ai_recommendations: List[str] = []
    todays_appointments: List[dict] = []
    pending_appointments: List[dict] = []


class DoctorProfileSchema(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    bio: Optional[str] = None
    experience_years: int = 0
    rating: float = 0.0
    total_reviews: int = 0
    is_active: bool = True


# Simple routes that work without database for now
@router.get("/dashboard", response_model=DashboardResponse)
async def get_doctor_dashboard(doctor_id: str = "doc-001"):
    """Get doctor dashboard with metrics and appointments"""
    try:
        # Return mock data for now
        return DashboardResponse(
            metrics=DashboardMetrics(
                total_appointments=25,
                todays_appointments=3,
                pending_appointments=5,
                total_prescriptions=12
            ),
            ai_workload_summary="Your workload is light today with 3 appointments scheduled.",
            ai_recommendations=[
                "Review pending lab results",
                "Follow up with yesterday's patients"
            ],
            todays_appointments=[],
            pending_appointments=[]
        )
        
    except Exception as e:
        logger.error(f"Error getting doctor dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load dashboard")


@router.get("/search", response_model=List[DoctorProfileSchema])
async def search_doctors(specialization: Optional[str] = None, name: Optional[str] = None):
    """Search for doctors by specialization or name"""
    try:
        # Return mock doctors for now
        mock_doctors = [
            DoctorProfileSchema(
                id="doc-001",
                name="Dr. Sarah Johnson",
                email="sarah.johnson@mentalhealth.com",
                phone="+1-555-0101",
                specialization="psychiatrist",
                bio="Board-certified psychiatrist with 15 years of experience in treating depression, anxiety, and mood disorders.",
                experience_years=15,
                rating=4.8,
                total_reviews=127,
                is_active=True
            ),
            DoctorProfileSchema(
                id="doc-002",
                name="Dr. Michael Chen",
                email="michael.chen@mentalhealth.com",
                phone="+1-555-0102",
                specialization="psychologist",
                bio="Clinical psychologist specializing in anxiety disorders, trauma, and PTSD.",
                experience_years=12,
                rating=4.9,
                total_reviews=98,
                is_active=True
            ),
            DoctorProfileSchema(
                id="doc-003",
                name="Dr. Emily Rodriguez",
                email="emily.rodriguez@mentalhealth.com",
                phone="+1-555-0103",
                specialization="therapist",
                bio="Licensed marriage and family therapist with expertise in relationship counseling.",
                experience_years=8,
                rating=4.7,
                total_reviews=76,
                is_active=True
            )
        ]
        
        # Filter by specialization if provided
        if specialization:
            mock_doctors = [doc for doc in mock_doctors if doc.specialization == specialization]
        
        # Filter by name if provided
        if name:
            mock_doctors = [doc for doc in mock_doctors if name.lower() in doc.name.lower()]
        
        return mock_doctors
        
    except Exception as e:
        logger.error(f"Error searching doctors: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to search doctors")


@router.get("/appointments")
async def get_appointments(doctor_id: str = "doc-001"):
    """Get all appointments for a doctor"""
    return {"appointments": [], "message": "Appointments endpoint working"}


@router.get("/patients")
async def get_patients(doctor_id: str = "doc-001"):
    """Get all patients for a doctor"""
    return {"patients": [], "message": "Patients endpoint working"}


@router.get("/prescriptions")
async def get_prescriptions(doctor_id: str = "doc-001"):
    """Get all prescriptions issued by a doctor"""
    return {"prescriptions": [], "message": "Prescriptions endpoint working"}


@router.get("/recommendations/{session_id}")
async def get_recommendations_for_session(session_id: str):
    """Get doctor recommendations for a chat session"""
    return {"recommendations": [], "message": "Recommendations endpoint working"}