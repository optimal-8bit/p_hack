"""Doctor-related API routes"""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from database.db import async_session_factory
from database.doctor_models import Doctor, Patient, Appointment, Prescription, DoctorRecommendation
from sqlalchemy import and_, or_

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/doctor", tags=["doctor"])


# Schemas
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


class PatientSchema(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None


class AppointmentSchema(BaseModel):
    id: str
    doctor_id: str
    patient_id: str
    scheduled_at: str
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: str
    created_at: str


class AppointmentCreateSchema(BaseModel):
    doctor_id: str
    patient_id: str
    scheduled_at: str
    reason: Optional[str] = None
    duration_minutes: int = 30


class AppointmentUpdateSchema(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class PrescriptionSchema(BaseModel):
    id: str
    doctor_id: str
    patient_id: str
    medicines: List[dict]
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    status: str
    issued_at: str


class DashboardMetrics(BaseModel):
    total_appointments: int
    todays_appointments: int
    pending_appointments: int
    total_prescriptions: int


class DashboardResponse(BaseModel):
    metrics: DashboardMetrics
    ai_workload_summary: str
    ai_recommendations: List[str]
    todays_appointments: List[AppointmentSchema]
    pending_appointments: List[AppointmentSchema]


class DoctorRecommendationSchema(BaseModel):
    id: str
    session_id: str
    recommended_specialization: Optional[str] = None
    reason: str
    urgency: str
    symptoms: Optional[List[str]] = None
    recommended_doctors: List[DoctorProfileSchema]
    is_crisis: bool
    created_at: str


# Routes
@router.get("/dashboard", response_model=DashboardResponse)
async def get_doctor_dashboard(doctor_id: str):
    """Get doctor dashboard with metrics and appointments"""
    try:
        async with async_session_factory() as db:
            # Get metrics
            total_appointments = db.query(Appointment).filter(
                Appointment.doctor_id == doctor_id
            ).count()
            
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            todays_appointments_query = db.query(Appointment).filter(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.scheduled_at >= today_start,
                    Appointment.scheduled_at < today_end
                )
            ).all()
            
            pending_appointments_query = db.query(Appointment).filter(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.status == 'pending'
                )
            ).order_by(Appointment.scheduled_at).limit(5).all()
            
            total_prescriptions = db.query(Prescription).filter(
                Prescription.doctor_id == doctor_id
            ).count()
            
            # Convert to schemas
            todays_appointments = [
                AppointmentSchema(
                    id=appt.id,
                    doctor_id=appt.doctor_id,
                    patient_id=appt.patient_id,
                    scheduled_at=appt.scheduled_at.isoformat(),
                    reason=appt.reason,
                    notes=appt.notes,
                    status=appt.status,
                    created_at=appt.created_at.isoformat()
                )
                for appt in todays_appointments_query
            ]
            
            pending_appointments = [
                AppointmentSchema(
                    id=appt.id,
                    doctor_id=appt.doctor_id,
                    patient_id=appt.patient_id,
                    scheduled_at=appt.scheduled_at.isoformat(),
                    reason=appt.reason,
                    notes=appt.notes,
                    status=appt.status,
                    created_at=appt.created_at.isoformat()
                )
                for appt in pending_appointments_query
            ]
            
            # Generate AI summary
            ai_summary = f"Your workload is {'light' if len(todays_appointments) < 5 else 'moderate' if len(todays_appointments) < 10 else 'heavy'} today with {len(todays_appointments)} appointments."
            
            ai_recommendations = []
            if len(pending_appointments) > 5:
                ai_recommendations.append("You have several pending appointments to review")
            if len(todays_appointments) > 8:
                ai_recommendations.append("Consider scheduling buffer time between appointments")
            
            return DashboardResponse(
                metrics=DashboardMetrics(
                    total_appointments=total_appointments,
                    todays_appointments=len(todays_appointments),
                    pending_appointments=len(pending_appointments_query),
                    total_prescriptions=total_prescriptions
                ),
                ai_workload_summary=ai_summary,
                ai_recommendations=ai_recommendations,
                todays_appointments=todays_appointments,
                pending_appointments=pending_appointments
        )
        
    except Exception as e:
        logger.error(f"Error getting doctor dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load dashboard")


@router.get("/appointments", response_model=List[AppointmentSchema])
async def get_appointments(doctor_id: str):
    """Get all appointments for a doctor"""
    try:
        async with async_session_factory() as db:
            appointments = db.query(Appointment).filter(
                Appointment.doctor_id == doctor_id
            ).order_by(Appointment.scheduled_at.desc()).all()
            
            return [
                AppointmentSchema(
                    id=appt.id,
                    doctor_id=appt.doctor_id,
                    patient_id=appt.patient_id,
                    scheduled_at=appt.scheduled_at.isoformat(),
                    reason=appt.reason,
                    notes=appt.notes,
                    status=appt.status,
                    created_at=appt.created_at.isoformat()
                )
                for appt in appointments
            ]
        
    except Exception as e:
        logger.error(f"Error getting appointments: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load appointments")


@router.post("/appointments", response_model=AppointmentSchema)
async def create_appointment(appointment: AppointmentCreateSchema):
    """Create a new appointment"""
    try:
        async with async_session_factory() as db:
            new_appointment = Appointment(
                doctor_id=appointment.doctor_id,
                patient_id=appointment.patient_id,
                scheduled_at=datetime.fromisoformat(appointment.scheduled_at),
                reason=appointment.reason,
                duration_minutes=appointment.duration_minutes,
                status='pending'
            )
            
            db.add(new_appointment)
            db.commit()
            db.refresh(new_appointment)
            
            return AppointmentSchema(
                id=new_appointment.id,
                doctor_id=new_appointment.doctor_id,
                patient_id=new_appointment.patient_id,
                scheduled_at=new_appointment.scheduled_at.isoformat(),
                reason=new_appointment.reason,
                notes=new_appointment.notes,
                status=new_appointment.status,
                created_at=new_appointment.created_at.isoformat()
            )
        
    except Exception as e:
        logger.error(f"Error creating appointment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create appointment")


@router.patch("/appointments/{appointment_id}", response_model=AppointmentSchema)
async def update_appointment(appointment_id: str, update: AppointmentUpdateSchema):
    """Update an appointment"""
    try:
        async with async_session_factory() as db:
            appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
            
            if not appointment:
                raise HTTPException(status_code=404, detail="Appointment not found")
            
            if update.status:
                appointment.status = update.status
            if update.notes:
                appointment.notes = update.notes
            
            await db.commit()
            await db.refresh(appointment)
            
            return AppointmentSchema(
                id=appointment.id,
                doctor_id=appointment.doctor_id,
                patient_id=appointment.patient_id,
                scheduled_at=appointment.scheduled_at.isoformat(),
                reason=appointment.reason,
                notes=appointment.notes,
                status=appointment.status,
                created_at=appointment.created_at.isoformat()
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating appointment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update appointment")


@router.get("/patients", response_model=List[PatientSchema])
async def get_patients(doctor_id: str):
    """Get all patients for a doctor (patients with appointments)"""
    try:
        async with async_session_factory() as db:
            # Get unique patient IDs from appointments
            patient_ids = db.query(Appointment.patient_id).filter(
                Appointment.doctor_id == doctor_id
            ).distinct().all()
            
            patient_ids = [pid[0] for pid in patient_ids]
            
            patients = db.query(Patient).filter(Patient.id.in_(patient_ids)).all()
            
            return [
                PatientSchema(
                    id=patient.id,
                    name=patient.name,
                    email=patient.email,
                    phone=patient.phone
                )
                for patient in patients
            ]
        
    except Exception as e:
        logger.error(f"Error getting patients: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load patients")


@router.get("/prescriptions", response_model=List[PrescriptionSchema])
async def get_prescriptions(doctor_id: str):
    """Get all prescriptions issued by a doctor"""
    try:
        async with async_session_factory() as db:
            prescriptions = db.query(Prescription).filter(
                Prescription.doctor_id == doctor_id
            ).order_by(Prescription.issued_at.desc()).all()
            
            return [
                PrescriptionSchema(
                    id=presc.id,
                    doctor_id=presc.doctor_id,
                    patient_id=presc.patient_id,
                    medicines=presc.medicines,
                    diagnosis=presc.diagnosis,
                    notes=presc.notes,
                    status=presc.status,
                    issued_at=presc.issued_at.isoformat()
                )
                for presc in prescriptions
            ]
        
    except Exception as e:
        logger.error(f"Error getting prescriptions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load prescriptions")


@router.get("/recommendations/{session_id}", response_model=List[DoctorRecommendationSchema])
async def get_recommendations_for_session(session_id: str):
    """Get doctor recommendations for a chat session"""
    try:
        async with async_session_factory() as db:
            recommendations = db.query(DoctorRecommendation).filter(
                DoctorRecommendation.session_id == session_id
            ).order_by(DoctorRecommendation.created_at.desc()).all()
            
            result = []
            for rec in recommendations:
                # Get recommended doctors
                doctor_ids = rec.recommended_doctors or []
                doctors = db.query(Doctor).filter(
                    and_(
                        Doctor.id.in_(doctor_ids),
                        Doctor.is_active == True
                    )
                ).all() if doctor_ids else []
                
                # If no specific doctors, get by specialization
                if not doctors and rec.recommended_specialization:
                    doctors = db.query(Doctor).filter(
                        and_(
                            Doctor.specialization == rec.recommended_specialization,
                            Doctor.is_active == True
                        )
                    ).order_by(Doctor.rating.desc()).limit(3).all()
                
                result.append(DoctorRecommendationSchema(
                    id=rec.id,
                    session_id=rec.session_id,
                    recommended_specialization=rec.recommended_specialization,
                    reason=rec.reason,
                    urgency=rec.urgency,
                    symptoms=rec.symptoms,
                    recommended_doctors=[
                        DoctorProfileSchema(
                            id=doc.id,
                            name=doc.name,
                            email=doc.email,
                            phone=doc.phone,
                            specialization=doc.specialization,
                            bio=doc.bio,
                            experience_years=doc.experience_years,
                            rating=doc.rating,
                            total_reviews=doc.total_reviews,
                            is_active=doc.is_active
                        )
                        for doc in doctors
                    ],
                    is_crisis=rec.is_crisis,
                    created_at=rec.created_at.isoformat()
                ))
            
            return result
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load recommendations")


@router.get("/search", response_model=List[DoctorProfileSchema])
async def search_doctors(specialization: Optional[str] = None, name: Optional[str] = None):
    """Search for doctors by specialization or name"""
    try:
        async with async_session_factory() as db:
            query = db.query(Doctor).filter(Doctor.is_active == True)
            
            if specialization:
                query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
            
            if name:
                query = query.filter(Doctor.name.ilike(f"%{name}%"))
            
            doctors = query.order_by(Doctor.rating.desc()).limit(10).all()
            
            return [
                DoctorProfileSchema(
                    id=doc.id,
                    name=doc.name,
                    email=doc.email,
                    phone=doc.phone,
                    specialization=doc.specialization,
                    bio=doc.bio,
                    experience_years=doc.experience_years,
                    rating=doc.rating,
                    total_reviews=doc.total_reviews,
                    is_active=doc.is_active
                )
                for doc in doctors
            ]
        
    except Exception as e:
        logger.error(f"Error searching doctors: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to search doctors")
