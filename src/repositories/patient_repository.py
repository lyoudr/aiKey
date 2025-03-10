from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import List

from src.models.database import get_db
from src.models.medical import Patient, PatientCost

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


def list_patient_cost(db: Session):
    results = (
        db.query(
            Patient.id.label("patient_id"),
            func.concat(Patient.first_name, " ", Patient.last_name).label("patient_name"),
            Patient.gender,
            PatientCost.total_cost.label("cost"),
            PatientCost.month,
            PatientCost.updated_time
        )
        .join(PatientCost, Patient.id == PatientCost.patient_id)
        .order_by(PatientCost.updated_time.desc())
        .all()
    )
    return results

def list_patient(db: Session) -> List:
    return db.query(Patient).order_by(Patient.id.asc()).all()