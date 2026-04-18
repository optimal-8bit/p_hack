import logging
import json
from typing import List, Dict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.models import Base, ChatSession, CrisisEvent, PrescriptionAnalysis, MedicineReminder
import config

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    config.DATABASE_URL,
    echo=False,
    future=True
)

# Create async session factory
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables():
    """Create all database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")


async def save_chat_turn(
    session_id: str,
    user_message: str,
    bot_response: str,
    emotion: str,
    intent: str,
    is_crisis: bool,
    language: str,
    processing_time: float
):
    """Save a chat turn to the database"""
    try:
        async with async_session_factory() as session:
            chat_turn = ChatSession(
                session_id=session_id,
                user_message=user_message,
                bot_response=bot_response,
                emotion=emotion,
                intent=intent,
                is_crisis=is_crisis,
                detected_language=language,
                processing_time_ms=processing_time
            )
            session.add(chat_turn)
            await session.commit()
            logger.debug(f"Saved chat turn for session {session_id}")
    except Exception as e:
        logger.error(f"Failed to save chat turn: {e}")


async def get_session_history(session_id: str) -> List[Dict]:
    """Get conversation history for a session"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(
                select(ChatSession)
                .where(ChatSession.session_id == session_id)
                .order_by(ChatSession.created_at)
            )
            turns = result.scalars().all()
            
            return [
                {
                    "user_message": turn.user_message,
                    "bot_response": turn.bot_response,
                    "emotion": turn.emotion,
                    "intent": turn.intent,
                    "timestamp": turn.created_at.isoformat(),
                }
                for turn in turns
            ]
    except Exception as e:
        logger.error(f"Failed to get session history: {e}")
        return []


async def save_crisis_event(session_id: str, crisis_type: str):
    """Save a crisis event (privacy-safe, no message content)"""
    try:
        async with async_session_factory() as session:
            crisis_event = CrisisEvent(
                session_id=session_id,
                crisis_type=crisis_type
            )
            session.add(crisis_event)
            await session.commit()
            logger.info(f"Saved crisis event: session={session_id}, type={crisis_type}")
    except Exception as e:
        logger.error(f"Failed to save crisis event: {e}")


# Prescription and Reminder functions

async def save_prescription_analysis(
    session_id: str,
    extracted_text: str,
    medicines: List[Dict],
    filename: str = None
) -> str:
    """Save prescription analysis to database"""
    try:
        async with async_session_factory() as session:
            prescription = PrescriptionAnalysis(
                session_id=session_id,
                filename=filename,
                extracted_text=extracted_text,
                medicines=json.dumps(medicines),
                notes="Prescription analyzed successfully"
            )
            session.add(prescription)
            await session.commit()
            await session.refresh(prescription)
            logger.info(f"Saved prescription analysis: {prescription.id}")
            return prescription.id
    except Exception as e:
        logger.error(f"Failed to save prescription analysis: {e}")
        raise


async def get_user_prescriptions(session_id: str) -> List[Dict]:
    """Get all prescriptions for a session"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(
                select(PrescriptionAnalysis)
                .where(PrescriptionAnalysis.session_id == session_id)
                .order_by(PrescriptionAnalysis.created_at.desc())
            )
            prescriptions = result.scalars().all()
            
            return [
                {
                    "prescription_id": p.id,
                    "filename": p.filename,
                    "extracted_text": p.extracted_text,
                    "medicines": json.loads(p.medicines),
                    "notes": p.notes,
                    "created_at": p.created_at.isoformat(),
                }
                for p in prescriptions
            ]
    except Exception as e:
        logger.error(f"Failed to get prescriptions: {e}")
        return []


async def save_reminder_schedule(
    session_id: str,
    prescription_id: str,
    medicine_name: str,
    dosage: str,
    time: str,
    instructions: str,
    doses_per_day: int
) -> str:
    """Save a medicine reminder"""
    try:
        async with async_session_factory() as session:
            reminder = MedicineReminder(
                session_id=session_id,
                prescription_id=prescription_id,
                medicine_name=medicine_name,
                dosage=dosage,
                time=time,
                instructions=instructions,
                doses_per_day=doses_per_day,
                doses_taken=0
            )
            session.add(reminder)
            await session.commit()
            await session.refresh(reminder)
            logger.info(f"Saved reminder: {reminder.id}")
            return reminder.id
    except Exception as e:
        logger.error(f"Failed to save reminder: {e}")
        raise


async def get_user_reminders(session_id: str) -> List[Dict]:
    """Get all reminders for a session"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(
                select(MedicineReminder)
                .where(MedicineReminder.session_id == session_id)
                .order_by(MedicineReminder.time)
            )
            reminders = result.scalars().all()
            
            return [
                {
                    "id": r.id,
                    "medicine_name": r.medicine_name,
                    "dosage": r.dosage,
                    "time": r.time,
                    "instructions": r.instructions,
                    "doses_per_day": int(r.doses_per_day),
                    "doses_taken": int(r.doses_taken),
                    "created_at": r.created_at.isoformat(),
                }
                for r in reminders
            ]
    except Exception as e:
        logger.error(f"Failed to get reminders: {e}")
        return []


async def update_reminder_dose(reminder_id: str, doses_taken: int):
    """Update doses taken for a reminder"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(
                select(MedicineReminder)
                .where(MedicineReminder.id == reminder_id)
            )
            reminder = result.scalar_one_or_none()
            
            if reminder:
                reminder.doses_taken = doses_taken
                await session.commit()
                logger.info(f"Updated reminder {reminder_id} doses to {doses_taken}")
            else:
                logger.warning(f"Reminder {reminder_id} not found")
    except Exception as e:
        logger.error(f"Failed to update reminder dose: {e}")
        raise


async def delete_reminder(reminder_id: str):
    """Delete a reminder"""
    try:
        async with async_session_factory() as session:
            result = await session.execute(
                select(MedicineReminder)
                .where(MedicineReminder.id == reminder_id)
            )
            reminder = result.scalar_one_or_none()
            
            if reminder:
                await session.delete(reminder)
                await session.commit()
                logger.info(f"Deleted reminder {reminder_id}")
            else:
                logger.warning(f"Reminder {reminder_id} not found")
    except Exception as e:
        logger.error(f"Failed to delete reminder: {e}")
        raise
