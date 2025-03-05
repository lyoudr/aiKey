from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int 

    class Config:
        orm_mode = True

