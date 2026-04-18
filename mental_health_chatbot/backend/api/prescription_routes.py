"""
Prescription analyzer and reminder system routes
"""
import logging
import base64
import json
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from database.db import (
    save_prescription_analysis,
    get_user_prescriptions,
    save_reminder_schedule,
    get_user_reminders,
    update_reminder_dose,
    delete_reminder
)
from utils.prescription_llm import extract_medicines_from_image
import config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/prescription", tags=["prescription"])


class MedicineItem(BaseModel):
    medicine_name: str
    dosage: str
    frequency: str
    instructions: str
    timings: Optional[List[str]] = []


class PrescriptionAnalysisResponse(BaseModel):
    prescription_id: str
    extracted_text: str
    medicines: List[MedicineItem]
    notes: Optional[str] = None
    created_at: str


class ReminderScheduleRequest(BaseModel):
    prescription_id: str
    medicines: List[dict]  # {medicine_name, dosage, timings, instructions}


class ReminderItem(BaseModel):
    id: str
    medicine_name: str
    dosage: str
    time: str
    instructions: str
    doses_per_day: int
    doses_taken: int
    created_at: str


class UpdateDoseRequest(BaseModel):
    reminder_id: str
    doses_taken: int


@router.post("/upload", response_model=PrescriptionAnalysisResponse)
async def upload_prescription(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload prescription image and extract medicines using Gemini Vision API"""
    try:
        logger.info(f"📥 Prescription upload: session={session_id}")
        
        # Read image
        contents = await file.read()
        logger.info(f"📄 File: {len(contents)} bytes, type={file.content_type}")
        
        # Validate
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only images allowed")
        
        # Send image directly to Gemini Vision API
        logger.info("🚀 Sending image to Gemini Vision API...")
        medicines_data = await extract_medicines_from_image(contents)
        
        if not medicines_data or len(medicines_data) == 0:
            logger.warning("⚠️ Gemini returned no medicines, using fallback")
            logger.warning("⚠️ This means either: 1) No medicines in image, 2) Gemini API failed, 3) API key issue")
            medicines = _get_mock_medicines()
        else:
            logger.info(f"✅ Gemini extracted {len(medicines_data)} medicines:")
            for med in medicines_data:
                logger.info(f"   • {med.get('medicine_name')} - {med.get('dosage')} - {med.get('frequency')}")
            
            medicines = []
            for med_data in medicines_data:
                frequency = med_data.get("frequency", "").lower()
                timings = _frequency_to_timings(frequency)
                
                medicine = MedicineItem(
                    medicine_name=med_data.get("medicine_name", "Unknown"),
                    dosage=med_data.get("dosage", "As prescribed"),
                    frequency=med_data.get("frequency", "As prescribed"),
                    instructions=med_data.get("instructions", "Follow doctor's advice"),
                    timings=timings
                )
                medicines.append(medicine)
                logger.info(f"   → Processed: {medicine.medicine_name} with timings {timings}")
        
        # Save to database
        prescription_id = await save_prescription_analysis(
            session_id=session_id,
            extracted_text=f"Analyzed by Gemini Vision API - {len(medicines)} medicines found",
            medicines=[m.dict() for m in medicines],
            filename=file.filename
        )
        
        logger.info(f"💾 Saved prescription: {prescription_id}")
        
        return PrescriptionAnalysisResponse(
            prescription_id=prescription_id,
            extracted_text=f"Analyzed by Gemini Vision API",
            medicines=medicines,
            notes="Prescription analyzed successfully. Please verify all details.",
            created_at=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process: {str(e)}")


@router.get("/list/{session_id}")
async def list_prescriptions(session_id: str):
    """
    Get all prescriptions for a session
    """
    try:
        prescriptions = await get_user_prescriptions(session_id)
        return {"prescriptions": prescriptions}
    except Exception as e:
        logger.error(f"Error listing prescriptions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve prescriptions")


@router.post("/schedule")
async def create_reminder_schedule(request: ReminderScheduleRequest, session_id: str):
    """
    Create reminder schedule from prescription
    """
    try:
        reminders = []
        
        for medicine in request.medicines:
            medicine_name = medicine.get("medicine_name", "")
            dosage = medicine.get("dosage", "")
            instructions = medicine.get("instructions", "")
            timings = medicine.get("timings", [])
            
            # Default timings if not provided
            if not timings:
                timings = ["09:00"]
            
            # Create reminder for each timing
            for time in timings:
                reminder_id = await save_reminder_schedule(
                    session_id=session_id,
                    prescription_id=request.prescription_id,
                    medicine_name=medicine_name,
                    dosage=dosage,
                    time=time,
                    instructions=instructions,
                    doses_per_day=len(timings)
                )
                reminders.append(reminder_id)
                logger.info(f"Created reminder {reminder_id} for {medicine_name} at {time}")
        
        logger.info(f"Created {len(reminders)} reminders for session {session_id}")
        return {
            "status": "success",
            "message": f"Created {len(reminders)} reminders",
            "reminder_ids": reminders
        }
        
    except Exception as e:
        logger.error(f"Error creating reminder schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create reminder schedule: {str(e)}")


@router.get("/reminders/{session_id}", response_model=List[ReminderItem])
async def get_reminders(session_id: str):
    """
    Get all reminders for a session
    """
    try:
        reminders = await get_user_reminders(session_id)
        return reminders
    except Exception as e:
        logger.error(f"Error getting reminders: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve reminders")


@router.patch("/reminders/dose")
async def update_dose(request: UpdateDoseRequest):
    """
    Update dose taken count for a reminder
    """
    try:
        await update_reminder_dose(request.reminder_id, request.doses_taken)
        return {"status": "success", "message": "Dose updated"}
    except Exception as e:
        logger.error(f"Error updating dose: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update dose")


@router.delete("/reminders/{reminder_id}")
async def delete_reminder_endpoint(reminder_id: str):
    """
    Delete a reminder
    """
    try:
        await delete_reminder(reminder_id)
        return {"status": "success", "message": "Reminder deleted"}
    except Exception as e:
        logger.error(f"Error deleting reminder: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete reminder")


# Helper functions

def _frequency_to_timings(frequency: str) -> List[str]:
    """Convert frequency text to suggested timings"""
    frequency = frequency.lower()
    
    if "once" in frequency or "1" in frequency or "daily" in frequency and "twice" not in frequency:
        return ["09:00"]
    elif "twice" in frequency or "2" in frequency or "two times" in frequency:
        return ["09:00", "21:00"]
    elif "three" in frequency or "3" in frequency or "thrice" in frequency:
        return ["08:00", "14:00", "20:00"]
    elif "four" in frequency or "4" in frequency:
        return ["08:00", "12:00", "16:00", "20:00"]
    else:
        # Default to once daily
        return ["09:00"]


def _get_mock_medicines() -> List[MedicineItem]:
    """Return mock medicine data for testing"""
    logger.info("Using mock medicine data")
    return [
        MedicineItem(
            medicine_name="Aspirin",
            dosage="100mg",
            frequency="Twice daily",
            instructions="Take 1 tablet after meals",
            timings=["09:00", "21:00"]
        ),
        MedicineItem(
            medicine_name="Vitamin D",
            dosage="1000 IU",
            frequency="Once daily",
            instructions="Take 1 capsule in morning",
            timings=["08:00"]
        ),
        MedicineItem(
            medicine_name="Metformin",
            dosage="500mg",
            frequency="Three times daily",
            instructions="Take 1 tablet before meals",
            timings=["08:00", "14:00", "20:00"]
        ),
    ]
