from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class Role(Base):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    users = relationship("User", back_populates="role", foreign_keys="[User.role_id]")
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")

# Import User at bottom to avoid circular import issues and allow relationship evaluation
from app.models.user import User  # noqa: F401
