from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from googleapiclient.discovery import build
from datetime import datetime
from typing import List 
import google.auth

from src.models.user import User
from src.models.database import get_db
from src.schemas.medical import ( 
    MedicalRecordBase, 
    MedicalAnalysisResponse
)
from src.repositories import medical_repository
from src.utils.authenticate import (
    get_current_user, 
    RoleChecker,
    ServiceAuth
)
from src.utils.decorator import cache_response
from src.core.config import get_settings

settings = get_settings()
router = APIRouter(tags=["medical"], prefix="/medical")


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


@router.post(
    "/",
    summary="Greate medical record by patient_id.", 
    response_model=MedicalRecordBase
)
def create_medical_record(
    payload: MedicalRecordBase,
    db: Session = Depends(get_db),
    role: bool = Depends(RoleChecker(['DOCTOR'])),
    user: User = Depends(get_current_user)
):
    new_record = medical_repository.create_medical_record(db, payload)
    return MedicalRecordBase.from_orm(new_record)


@router.post(
    "/analysis",
    summary = "Run medical record analysis.",
    response_model=MedicalAnalysisResponse,
)
def medical_analysis(
    auth: bool = Depends(ServiceAuth())
):
    credentials, project_id = google.auth.default()
    dataflow = build('dataflow', 'v1b3', credentials=credentials)
    template_path = f"gs://{settings.GCS_BUCKET}/templates/medical_service_template"
    region = settings.REGION 
    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    job_request = {
        "jobName": f"medical_analysis_{current_date}",
        "environment": {
            "tempLocation": f"gs://{settings.GCS_BUCKET}/temp",
            "zone": "asia-east1-a"
        }
    }
    result = dataflow.projects().locations().templates().launch(
        projectId=project_id,
        location=region,
        gcsPath=template_path,
        body=job_request
    ).execute()
    return MedicalAnalysisResponse(status="Run medical analysis successfully.")