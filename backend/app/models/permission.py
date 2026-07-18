from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class Permission(Base):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
