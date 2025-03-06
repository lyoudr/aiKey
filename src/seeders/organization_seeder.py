from datetime import datetime 

from src.repositories import organization_repository
from src.models.database import get_db
from src.models.organization import Hospital

def seed():
    # Sample data for hospitals
    hospital_data = [
        {"name": "Springfield General Hospital", "address": "100 Main St, Springfield"},
        {"name": "Riverside Medical Center", "address": "200 River Rd, Riverside"},
        {"name": "Lakeside Health Institute", "address": "300 Lake Dr, Lakeside"},
    ]

    # Insert hospitals first
    organization_repository.batch_insert_hospital(hospital_data)

    # Retrieve inserted hospitals to map their IDs
    db = next(get_db())
    hospitals = db.query(Hospital).all()

    # Sample data for organizations (departments within hospitals)
    organization_data = [
        {"name": "Cardiology", "hospital_id": hospitals[0].id},
        {"name": "Neurology", "hospital_id": hospitals[0].id},
        {"name": "Oncology", "hospital_id": hospitals[1].id},
        {"name": "Pediatrics", "hospital_id": hospitals[1].id},
        {"name": "Emergency", "hospital_id": hospitals[2].id},
    ]

    # Insert organizations
    organization_repository.batch_insert_organization(organization_data)

    print("Seed data inserted successfully.")