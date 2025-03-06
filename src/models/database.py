from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import create_engine

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

meta = MetaData()
Base = declarative_base(metadata=meta)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from .user import User
from .role import Role, Permission
from .organization import Hospital, Organization
from .medical import Patient, PatientCost, MedicalRecord