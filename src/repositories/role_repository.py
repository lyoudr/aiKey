from sqlalchemy.orm import Session

from src.models.database import get_db
from src.models.role import Role, Permission
from src.models.user import User


def batch_insert_roles(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Role, data)
    db.commit()


def batch_insert_permissions(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Permission, data)
    db.commit()


def get_role_by_user(db: Session, user: User):
    return db.query(Role).filter(Role.id == user.role_id).first()