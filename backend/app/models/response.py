from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class UserResponse(Base):
    __tablename__ = "user_responses"

    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    session = relationship("AssessmentSession", back_populates="responses")
    user = relationship("User", back_populates="responses", foreign_keys=[user_id])
    question = relationship("Question", back_populates="responses")
    answer = relationship("Answer", back_populates="responses")

# Import related classes at bottom to avoid circular import issues and allow relationship evaluation
from app.models.session import AssessmentSession  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.question import Question  # noqa: F401
from app.models.answer import Answer  # noqa: F401
