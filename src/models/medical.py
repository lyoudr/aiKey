from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    ForeignKey,
    Date,
    String,
    Text,
    Enum,
    DateTime,
    func,
    DECIMAL,
    UniqueConstraint,
)
from src.models.database import Base


class Patient(Base):
    __tablename__ = "patient"

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum("MALE", "FEMALE", "OTHER", name="gender_enum"), nullable=False)
    contact_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    email = Column(String(100), nullable=True, unique=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PatientCost(Base):
    __tablename__ = "patient_cost"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patient.id"), nullable=False, index=True)
    month = Column(String(7), nullable=False)  # Format: 'YYYY-MM'
    total_cost = Column(DECIMAL(10, 2), nullable=False)

    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("patient_id", "month", name="unique_patient_month"),)



class MedicalRecord(Base):
    __tablename__ = "medical_record"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patient.id', ondelete="CASCADE"), nullable=False)
    record_date = Column(Date, nullable=False)
    diagnosis = Column(String(255), nullable=False)
    treatment = Column(String(255), nullable=True) # 療法
    prescription = Column(String(255), nullable=True) # 處方籤
    cost = Column(DECIMAL(65, 2), nullable=True)
    notes = Column(Text, nullable=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())