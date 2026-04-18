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
        from datetime import datetime, date
        
        # Get all appointments for this doctor
        doctor_appointments = [
            apt for apt in appointments_db.values()
            if apt["doctor_id"] == doctor_id
        ]
        
        # Calculate metrics
        total_appointments = len(doctor_appointments)
        pending_appointments = len([a for a in doctor_appointments if a["status"] == "pending"])
        
        # Get today's appointments
        today = date.today().isoformat()
        todays_appointments = [
            a for a in doctor_appointments
            if a["scheduled_at"].startswith(today)
        ]
        
        # Sort appointments by scheduled_at
        todays_appointments.sort(key=lambda x: x["scheduled_at"])
        pending_list = [a for a in doctor_appointments if a["status"] == "pending"]
        pending_list.sort(key=lambda x: x["scheduled_at"])
        
        # Generate AI summary
        if len(todays_appointments) == 0:
            workload_summary = "You have no appointments scheduled for today. Great time to catch up on paperwork!"
        elif len(todays_appointments) <= 3:
            workload_summary = f"Your workload is light today with {len(todays_appointments)} appointment(s) scheduled."
        else:
            workload_summary = f"You have a busy day ahead with {len(todays_appointments)} appointments scheduled."
        
        recommendations = []
        if pending_appointments > 0:
            recommendations.append(f"You have {pending_appointments} pending appointment(s) awaiting confirmation")
        if len(todays_appointments) > 0:
            recommendations.append("Review patient histories before today's appointments")
        
        return DashboardResponse(
            metrics=DashboardMetrics(
                total_appointments=total_appointments,
                todays_appointments=len(todays_appointments),
                pending_appointments=pending_appointments,
                total_prescriptions=0  # TODO: Implement prescriptions
            ),
            ai_workload_summary=workload_summary,
            ai_recommendations=recommendations,
            todays_appointments=todays_appointments[:5],  # Limit to 5
            pending_appointments=pending_list[:5]  # Limit to 5
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


class AppointmentCreate(BaseModel):
    doctor_id: str
    patient_id: Optional[str] = None
    session_id: Optional[str] = None
    scheduled_date: str  # ISO date string
    scheduled_time: str  # HH:MM format
    reason: str
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: str
    doctor_id: str
    patient_id: Optional[str]
    session_id: Optional[str]
    scheduled_at: str
    reason: str
    notes: Optional[str]
    status: str
    created_at: str


# In-memory appointments storage (replace with database later)
appointments_db = {}


@router.post("/appointments", response_model=AppointmentResponse)
async def create_appointment(appointment: AppointmentCreate):
    """Create a new appointment"""
    try:
        from datetime import datetime
        import uuid
        
        # Combine date and time
        scheduled_datetime = f"{appointment.scheduled_date}T{appointment.scheduled_time}:00"
        
        # Create appointment
        appointment_id = str(uuid.uuid4())
        new_appointment = {
            "id": appointment_id,
            "doctor_id": appointment.doctor_id,
            "patient_id": appointment.patient_id,
            "session_id": appointment.session_id,
            "scheduled_at": scheduled_datetime,
            "reason": appointment.reason,
            "notes": appointment.notes,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
        }
        
        appointments_db[appointment_id] = new_appointment
        
        logger.info(f"✅ Appointment created: {appointment_id} for doctor {appointment.doctor_id}")
        
        return AppointmentResponse(**new_appointment)
        
    except Exception as e:
        logger.error(f"Error creating appointment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create appointment")


@router.get("/appointments")
async def get_appointments(doctor_id: str = "doc-001"):
    """Get all appointments for a doctor"""
    try:
        # Filter appointments by doctor_id
        doctor_appointments = [
            apt for apt in appointments_db.values()
            if apt["doctor_id"] == doctor_id
        ]
        
        # Sort by scheduled_at (most recent first)
        doctor_appointments.sort(key=lambda x: x["scheduled_at"], reverse=True)
        
        return {"appointments": doctor_appointments, "total": len(doctor_appointments)}
        
    except Exception as e:
        logger.error(f"Error fetching appointments: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch appointments")


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