from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List 

from models.database import get_db
from schemas.medical import MedicalRecordBase
from repositories import medical_repository

router = APIRouter(tags=["medical"], prefix="/medicals")


@router.get("/{patient_id}", response_model=List[MedicalRecordBase])
def list_medical_record(
    patient_id: int,
    db: Session = Depends(get_db)
):
    records = medical_repository.list_medical_record(db, patient_id)
    return [MedicalRecordBase.from_orm(record) for record in records]