from src.models.database import get_db
from src.models.organization import Hospital, Organization

def batch_insert_hospital(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Hospital, data)
    db.commit()

def batch_insert_organization(data: list):
    db = next(get_db())
    db.bulk_insert_mappings(Organization, data)
    db.commit()