from fastapi import status, HTTPException
from sqlalchemy.orm import Session, joinedload

from src.models.database import get_db
from src.models.user import User
from src.models.role import Role

def batch_insert_users(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(User, data)
    db.commit()

def list_users(db: Session):
    return db.query(User).order_by(User.id).all()

def get_user_by_name(db: Session, username: str):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(
            detail=f'Can not get user : {username}',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
