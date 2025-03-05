from sqlalchemy.orm import Session

from models.user import User

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()