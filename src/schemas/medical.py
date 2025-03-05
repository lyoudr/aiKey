from pydantic import BaseModel
from datetime import date 
from typing import Optional


class MedicalRecordBase(BaseModel):
    patient_id: int
    record_date: date
    diagnosis: str
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    cost: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True