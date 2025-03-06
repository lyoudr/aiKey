from datetime import date, timedelta
import random
from src.repositories import medical_repository

def seed():
    diagnoses = ["Flu", "Diabetes", "Hypertension", "Asthma", "COVID-19", "Allergy", "Pneumonia"]
    treatments = ["Rest and hydration", "Insulin therapy", "Blood pressure medication", "Inhaler treatment", "Antiviral medication", "Antihistamines", "Antibiotics"]
    prescriptions = ["Paracetamol", "Metformin", "Lisinopril", "Albuterol", "Oseltamivir", "Loratadine", "Azithromycin"]

    # Sample patient IDs (Assuming we have these in the database)
    patient_ids = [1, 2, 3, 4]

    medical_records = []

    for patient_id in patient_ids:
        num_records = random.randint(2, 5)

        for _ in range(num_records):
            record = {
                "patient_id": patient_id,
                "record_date": date.today() - timedelta(days=random.randint(0, 365)),  # Random date within last year
                "diagnosis": random.choice(diagnoses),
                "treatment": random.choice(treatments) if random.random() > 0.2 else None,  # 80% chance to have treatment
                "prescription": random.choice(prescriptions) if random.random() > 0.3 else None,  # 70% chance to have prescription
                "cost": round(random.uniform(50, 500), 2) if random.random() > 0.1 else None,  # 90% chance to have cost
                "notes": "Follow-up required" if random.random() > 0.7 else None  # 30% chance to have notes
            }
            medical_records.append(record)
    
    medical_repository.batch_insert(medical_records)
