from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    Table,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from models.database import Base

role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id"), primary_key=True),
)

class Role(Base):
    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Permission(Base):
    __tablename__ = "permission"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())