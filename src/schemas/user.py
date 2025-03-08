from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int 
    name: str
    email: str
    user_type: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str