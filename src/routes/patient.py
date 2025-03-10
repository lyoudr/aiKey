from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.models.user import User
from src.schemas.patient import PatientBase, PatientCostBase
from src.repositories import patient_repository
from src.utils.authenticate import get_current_user, RoleChecker
from src.utils.decorator import cache_response

router = APIRouter(tags=["patient"], prefix="/patients")

@router.get(
    "/",
    summary="List patients.",
    response_model=List[PatientBase]
)
@cache_response(cache_key_func=lambda db, role, user: "patients_list")
def list_patients(
    db: Session = Depends(get_db),
    role: bool = Depends(RoleChecker(['ADMIN', 'DOCTOR'])),
    user: User = Depends(get_current_user)
):
    patients = patient_repository.list_patient(db)
    return [PatientBase.from_orm(patient) for patient in patients]


@router.get(
    "/info/{patient_id}",
    summary="Get patient by id.", 
    response_model=PatientBase
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    role: bool = Depends(RoleChecker(['ADMIN', 'DOCTOR']))
):
    patient = patient_repository.get_patient(db, patient_id)
    return patient


@router.get(
    "/cost",
    summary="List patient cost",
    response_model=List[PatientCostBase]
)
def patient_cost(
    db: Session = Depends(get_db),
    role: bool = Depends(RoleChecker(['ADMIN', 'DOCTOR'])),
    user: User = Depends(get_current_user)
):
    patient_costs = patient_repository.list_patient_cost(db)
    return [PatientCostBase(**dict(row._mapping)) for row in patient_costs]