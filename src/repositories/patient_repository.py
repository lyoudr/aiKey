from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.models.medical import Patient

def batch_insert(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Patient, data)
    db.commit()


def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            detail=f"Patient not found {patient_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return patient


def list_patient(db: Session) -> List:
    return db.query(Patient).order_by(Patient.id.asc()).all()