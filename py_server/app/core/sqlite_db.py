"""
SQLite database setup for offline diagnosis storage.
"""
import sqlite3
from pathlib import Path
from typing import Optional
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent.parent.parent / "diagnosis.db"


def get_sqlite_connection() -> sqlite3.Connection:
    """Get SQLite database connection."""
    conn = sqlite3.Connection(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_sqlite_db() -> None:
    """Initialize SQLite database with diagnosis_history table."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            risk_level TEXT NOT NULL,
            explanation TEXT,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def save_diagnosis(
    symptoms: str,
    prediction: str,
    confidence: float,
    risk_level: str,
    explanation: str,
    image_path: Optional[str] = None
) -> int:
    """
    Save diagnosis to SQLite database.
    
    Args:
        symptoms: Comma-separated symptoms
        prediction: Predicted disease
        confidence: Confidence score (0-1)
        risk_level: Risk level (Low/Medium/High)
        explanation: Explanation text
        image_path: Optional path to uploaded image
        
    Returns:
        ID of inserted record
    """
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO diagnosis_history 
        (symptoms, prediction, confidence, risk_level, explanation, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (symptoms, prediction, confidence, risk_level, explanation, image_path))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return record_id


def get_diagnosis_history(limit: int = 10) -> list[dict]:
    """
    Get recent diagnosis history.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of diagnosis records
    """
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, symptoms, prediction, confidence, risk_level, 
               explanation, image_path, timestamp
        FROM diagnosis_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
