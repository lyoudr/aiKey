from fastapi import status, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List 

from src.models.database import get_db
from src.models.medical import MedicalRecord

def batch_insert(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(MedicalRecord, data)
    db.commit()


def get_medical_record(db: Session, record_id: int) -> MedicalRecord:
    medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not medical_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Can not find medical record: {record_id}'
        )
    return medical_record


def list_medical_record(db: Session, patient_id: int) -> List:
    return db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.patient_id == patient_id
    ).order_by(
        desc(MedicalRecord.updated_time)
    ).all()