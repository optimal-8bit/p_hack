"""Seed script to populate sample doctors in the database"""
import asyncio
import sys
from database.db import async_session_factory, create_tables
from database.doctor_models import Doctor, Patient


async def seed_doctors():
    """Add sample doctors to the database"""
    print("Creating database tables...")
    await create_tables()
    
    print("Seeding sample doctors...")
    
    sample_doctors = [
        {
            "user_id": "doc-001",
            "name": "Dr. Sarah Johnson",
            "email": "sarah.johnson@mentalhealth.com",
            "phone": "+1-555-0101",
            "specialization": "psychiatrist",
            "license_number": "PSY-12345",
            "bio": "Board-certified psychiatrist with 15 years of experience in treating depression, anxiety, and mood disorders. Specializes in medication management and cognitive behavioral therapy.",
            "experience_years": 15,
            "rating": 4.8,
            "total_reviews": 127,
            "is_active": True
        },
        {
            "user_id": "doc-002",
            "name": "Dr. Michael Chen",
            "email": "michael.chen@mentalhealth.com",
            "phone": "+1-555-0102",
            "specialization": "psychologist",
            "license_number": "PSY-23456",
            "bio": "Clinical psychologist specializing in anxiety disorders, trauma, and PTSD. Uses evidence-based approaches including CBT and EMDR.",
            "experience_years": 12,
            "rating": 4.9,
            "total_reviews": 98,
            "is_active": True
        },
        {
            "user_id": "doc-003",
            "name": "Dr. Emily Rodriguez",
            "email": "emily.rodriguez@mentalhealth.com",
            "phone": "+1-555-0103",
            "specialization": "therapist",
            "license_number": "LMFT-34567",
            "bio": "Licensed marriage and family therapist with expertise in relationship counseling, family dynamics, and stress management.",
            "experience_years": 8,
            "rating": 4.7,
            "total_reviews": 76,
            "is_active": True
        },
        {
            "user_id": "doc-004",
            "name": "Dr. James Williams",
            "email": "james.williams@mentalhealth.com",
            "phone": "+1-555-0104",
            "specialization": "psychiatrist",
            "license_number": "PSY-45678",
            "bio": "Psychiatrist specializing in severe mental illness, crisis intervention, and medication management. Available for urgent consultations.",
            "experience_years": 20,
            "rating": 4.9,
            "total_reviews": 156,
            "is_active": True
        },
        {
            "user_id": "doc-005",
            "name": "Dr. Lisa Anderson",
            "email": "lisa.anderson@mentalhealth.com",
            "phone": "+1-555-0105",
            "specialization": "psychologist",
            "license_number": "PSY-56789",
            "bio": "Child and adolescent psychologist with focus on developmental issues, behavioral problems, and family therapy.",
            "experience_years": 10,
            "rating": 4.8,
            "total_reviews": 89,
            "is_active": True
        },
        {
            "user_id": "doc-006",
            "name": "Dr. Robert Taylor",
            "email": "robert.taylor@mentalhealth.com",
            "phone": "+1-555-0106",
            "specialization": "general_practitioner",
            "license_number": "MD-67890",
            "bio": "General practitioner with interest in mental health. Can provide initial assessments and referrals to specialists.",
            "experience_years": 18,
            "rating": 4.6,
            "total_reviews": 134,
            "is_active": True
        }
    ]
    
    async with async_session_factory() as session:
        for doctor_data in sample_doctors:
            # Check if doctor already exists
            existing = await session.execute(
                f"SELECT id FROM doctors WHERE email = '{doctor_data['email']}'"
            )
            if existing.first():
                print(f"  ⏭️  Skipping {doctor_data['name']} (already exists)")
                continue
            
            doctor = Doctor(**doctor_data)
            session.add(doctor)
            print(f"  ✅ Added {doctor_data['name']} ({doctor_data['specialization']})")
        
        await session.commit()
    
    print(f"\n✅ Successfully seeded {len(sample_doctors)} doctors!")
    print("\nYou can now:")
    print("  1. View doctors at: GET /api/doctor/search")
    print("  2. Get recommendations in chat sessions")
    print("  3. Access doctor dashboard at: GET /api/doctor/dashboard?doctor_id=<id>")


if __name__ == "__main__":
    try:
        asyncio.run(seed_doctors())
    except KeyboardInterrupt:
        print("\n\nSeeding cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error seeding doctors: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
