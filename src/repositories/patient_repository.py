from sqlalchemy.orm import Session
from typing import List

from models.database import get_db
from models.medical import Patient

def batch_insert(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Patient, data)
    db.commit()


def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise Exception 
    return patient


def list_patient(db: Session) -> List:
    return db.query(Patient).order_by(Patient.id.asc()).all()