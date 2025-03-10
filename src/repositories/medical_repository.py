from fastapi import status, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List 

from src.models.database import get_db
from src.models.medical import MedicalRecord
from src.schemas.medical import MedicalRecordBase

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


def create_medical_record(db: Session, payload: MedicalRecordBase):
    try:
        new_record = MedicalRecord(
            patient_id=payload.patient_id,
            record_date=payload.record_date,
            diagnosis=payload.diagnosis,
            treatment=payload.treatment,
            prescription=payload.prescription,
            cost=payload.cost,
            notes=payload.notes,
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)  # Fetch updated values like ID and timestamps

        return new_record
    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(
            detail=f"Create medical record error: {e}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )