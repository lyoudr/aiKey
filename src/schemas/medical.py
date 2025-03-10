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
    
    # Override the dict method to convert the date to string 
    def dict(self, **kwargs):
        record_dict = super().dict(**kwargs)
        if isinstance(record_dict.get("record_date"), date):
            record_dict["record_date"] = record_dict["record_date"].isoformat()
        return record_dict


class MedicalAnalysisResponse(BaseModel):
    status: str


