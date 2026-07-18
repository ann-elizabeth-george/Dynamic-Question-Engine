from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    profile = relationship("UserProfile", back_populates="user", uselist=False, foreign_keys="[UserProfile.user_id]")
    sessions = relationship("AssessmentSession", back_populates="user", foreign_keys="[AssessmentSession.user_id]")
    responses = relationship("UserResponse", back_populates="user", foreign_keys="[UserResponse.user_id]")

# Import related classes at bottom to avoid circular import issues and allow relationship evaluation
from app.models.user_profile import UserProfile  # noqa: F401
from app.models.session import AssessmentSession  # noqa: F401
from app.models.response import UserResponse  # noqa: F401
