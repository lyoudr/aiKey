from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    Enum,
    DateTime,
    func,
)
from src.models.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    user_type = Column(Enum("AIPHAS", "DOCTOR", name="user_type_enum"), nullable=False)
    role_id = Column(
        BigInteger, 
        ForeignKey("role.id", ondelete="CASCADE"),
        nullable=True
    )
    organization_id = Column(
        BigInteger,
        ForeignKey("organization.id", ondelete="SET NULL"),
        nullable=True
    )
    hashed_password = Column(String, nullable=False)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
