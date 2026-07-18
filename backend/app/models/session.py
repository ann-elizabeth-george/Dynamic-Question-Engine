from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    current_question_index = Column(Integer, default=0, nullable=False)
    current_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    status = Column(String(50), default="STARTED", nullable=False)  # STARTED, COMPLETED
    start_time = Column(DateTime, nullable=False)
    completion_time = Column(DateTime, nullable=True)
    progress_percentage = Column(Numeric(5, 2), default=0.00, nullable=False)

    user = relationship("User", back_populates="sessions", foreign_keys=[user_id])
    category = relationship("Category", back_populates="sessions")
    responses = relationship("UserResponse", back_populates="session")

# Import related classes at bottom to avoid circular import issues and allow relationship evaluation
from app.models.user import User  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.response import UserResponse  # noqa: F401
