from src.models.database import get_db
from src.models.role import Role, Permission


def batch_insert_roles(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Role, data)
    db.commit()


def batch_insert_permissions(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Permission, data)
    db.commit()