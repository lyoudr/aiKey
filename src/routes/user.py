from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.models.user import User
from src.schemas.user import UserResponse
from src.repositories import user_repository
from src.utils.authenticate import get_current_user, RoleChecker

router = APIRouter(tags=["user"], prefix="/user")

@router.get(
    "/",
    summary="List users",
    response_model=List[UserResponse]
)
def list_user(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    role: bool = Depends(RoleChecker(['ADMIN']))
):
    users = user_repository.list_users(db)
    return users


@router.get(
    "/{user_id}",
    summary="Get user by id",
    response_model=UserResponse
)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    role: bool = Depends(RoleChecker(['ADMIN']))
):
    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            detail=f"User not found {user_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user