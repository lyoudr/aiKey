from sqlalchemy.orm import Session

from src.models.database import get_db
from src.models.user import User


def batch_insert_users(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(User, data)
    db.commit()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()