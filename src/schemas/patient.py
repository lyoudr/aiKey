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