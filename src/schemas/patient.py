from pydantic import BaseModel
from datetime import date
from typing import Optional



class PatientBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    contact_number: Optional[str] 
    address: Optional[str]
    email: Optional[str]

    class Config:
        orm_mode = True
    
    # Override the dict method to convert the date to string 
    def dict(self, **kwargs):
        record_dict = super().dict(**kwargs)
        if isinstance(record_dict.get("date_of_birth"), date):
            record_dict["date_of_birth"] = record_dict["date_of_birth"].isoformat()
        return record_dict