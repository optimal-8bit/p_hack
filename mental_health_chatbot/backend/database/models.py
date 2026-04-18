import uuid
import json
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatSession(Base):
    """Chat session table - stores all conversation turns"""
    __tablename__ = "chat_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), index=True, nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    emotion = Column(String(50), nullable=False)
    intent = Column(String(100), nullable=False)
    is_crisis = Column(Boolean, default=False, nullable=False)
    detected_language = Column(String(10), nullable=False)
    processing_time_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CrisisEvent(Base):
    """Crisis events table - privacy-safe crisis log (no message content)"""
    __tablename__ = "crisis_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), nullable=False)
    crisis_type = Column(String(50), nullable=False)  # "suicide", "self_harm", "general_distress"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class PrescriptionAnalysis(Base):
    """Prescription analysis table - stores uploaded prescriptions and extracted data"""
    __tablename__ = "prescription_analyses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), index=True, nullable=False)
    filename = Column(String(255), nullable=True)
    extracted_text = Column(Text, nullable=False)
    medicines = Column(Text, nullable=False)  # JSON string of medicines list
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MedicineReminder(Base):
    """Medicine reminder table - stores reminder schedules"""
    __tablename__ = "medicine_reminders"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), index=True, nullable=False)
    prescription_id = Column(String(36), nullable=True)
    medicine_name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)
    time = Column(String(10), nullable=False)  # HH:MM format
    instructions = Column(Text, nullable=True)
    doses_per_day = Column(Float, default=1, nullable=False)
    doses_taken = Column(Float, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
