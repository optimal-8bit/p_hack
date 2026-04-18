import logging
from typing import List, Dict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.models import Base, ChatSession, CrisisEvent
from database.doctor_models import Doctor, Patient, Appointment, Prescription, DoctorRecommendation
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


async def get_db_session():
    """Get database session context manager"""
    async with async_session_factory() as session:
        yield session
