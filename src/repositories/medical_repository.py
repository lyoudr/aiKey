from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List 

from src.models.medical import MedicalRecord


def get_medical_record(db: Session, record_id: int) -> MedicalRecord:
    medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not medical_record:
        raise Exception
    return medical_record


def list_medical_record(db: Session, patient_id: int) -> List:
    return db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.patient_id == patient_id
    ).order_by(
        desc(MedicalRecord.updated_time)
    ).all()