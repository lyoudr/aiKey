from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models.database import get_db
from schemas.patient import PatientBase
from repositories import patient_repository


router = APIRouter(tags=["patient"], prefix="/patients")

@router.get("/", response_model=List[PatientBase])
def list_patients(
    db: Session = Depends(get_db)
):
    patients = patient_repository.list_patient(db)
    return [PatientBase.from_orm(patient) for patient in patients]


@router.get("/{patient_id}", response_model=PatientBase)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = patient_repository.get_patient(db, patient_id)
    return patient