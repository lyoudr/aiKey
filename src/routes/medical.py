from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List 

from src.models.user import User
from src.models.database import get_db
from src.schemas.medical import MedicalRecordBase
from src.repositories import medical_repository
from src.utils.authenticate import get_current_user, RoleChecker
from src.utils.decorator import cache_response


router = APIRouter(tags=["medical"], prefix="/medicals")

@router.get(
    "/{patient_id}",
    summary="Get medical record by patient_id.", 
    response_model=List[MedicalRecordBase]
)
@cache_response(
    cache_key_func=lambda patient_id, db, role, user: f"medical_records:{patient_id}"
)
def list_medical_record(
    patient_id: int,
    db: Session = Depends(get_db),
    role: bool = Depends(RoleChecker(['DOCTOR'])),
    user: User = Depends(get_current_user),
):
    # If data not in cache, fetch from database
    records = medical_repository.list_medical_record(db, patient_id)
    return [MedicalRecordBase.from_orm(record) for record in records]