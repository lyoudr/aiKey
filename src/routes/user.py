from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.user import UserResponse
from src.repositories import user_repository

router = APIRouter(tags=["user"], prefix="/user")

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_repository.get_user(db, user_id)
    if user is None:
        return {"error": "User not found"}
    return user