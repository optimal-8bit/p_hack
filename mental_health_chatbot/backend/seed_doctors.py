"""Seed script to create doctor accounts"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import after path is set
from api.auth_routes import users_db, hash_password
import uuid
from datetime import datetime

def seed_doctors():
    """Create sample doctor accounts"""
    
    doctors = [
        {
            "name": "Dr. Sarah Johnson",
            "email": "sarah.johnson@mediscan.com",
            "password": "doctor123",
            "role": "doctor",
            "specialization": "psychiatrist",
            "experience_years": 15,
            "bio": "Board-certified psychiatrist with 15 years of experience in treating depression, anxiety, and mood disorders."
        },
        {
            "name": "Dr. Michael Chen",
            "email": "michael.chen@mediscan.com",
            "password": "doctor123",
            "role": "doctor",
            "specialization": "psychologist",
            "experience_years": 12,
            "bio": "Clinical psychologist specializing in anxiety disorders, trauma, and PTSD."
        },
        {
            "name": "Dr. Emily Rodriguez",
            "email": "emily.rodriguez@mediscan.com",
            "password": "doctor123",
            "role": "doctor",
            "specialization": "therapist",
            "experience_years": 8,
            "bio": "Licensed marriage and family therapist with expertise in relationship counseling."
        },
        {
            "name": "Dr. Rajesh Kumar",
            "email": "rajesh.kumar@mediscan.com",
            "password": "doctor123",
            "role": "doctor",
            "specialization": "psychiatrist",
            "experience_years": 20,
            "bio": "Senior psychiatrist specializing in severe mental health conditions and medication management."
        },
        {
            "name": "Dr. Priya Sharma",
            "email": "priya.sharma@mediscan.com",
            "password": "doctor123",
            "role": "doctor",
            "specialization": "psychologist",
            "experience_years": 10,
            "bio": "Child and adolescent psychologist with focus on anxiety and behavioral issues."
        }
    ]
    
    print("=" * 60)
    print("Seeding Doctor Accounts")
    print("=" * 60)
    
    for doctor_data in doctors:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": doctor_data["name"],
            "email": doctor_data["email"],
            "password": hash_password(doctor_data["password"]),
            "role": "doctor",
            "specialization": doctor_data["specialization"],
            "experience_years": doctor_data["experience_years"],
            "bio": doctor_data["bio"],
            "created_at": datetime.utcnow().isoformat(),
        }
        users_db[user_id] = user
        print(f"✅ Created: {doctor_data['name']} ({doctor_data['specialization']})")
        print(f"   Email: {doctor_data['email']}")
        print(f"   Password: {doctor_data['password']}")
        print()
    
    print("=" * 60)
    print(f"Total doctors created: {len(doctors)}")
    print("=" * 60)
    print("\nYou can now login with any of these accounts:")
    print("Email: sarah.johnson@mediscan.com")
    print("Password: doctor123")
    print("=" * 60)

if __name__ == "__main__":
    seed_doctors()
