from sqlalchemy import (
    Column, 
    BigInteger,
    String, 
    DateTime,
    ForeignKey, 
    func
)

from src.models.database import Base


class Hospital(Base):
    __tablename__ = "hospital"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(500), nullable=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Organization(Base):
    __tablename__ = "organization"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    hospital_id = Column(
        BigInteger,
        ForeignKey("hospital.id", ondelete="CASCADE"),  # If a hospital is deleted, its departments are deleted
        nullable=False
    )
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())