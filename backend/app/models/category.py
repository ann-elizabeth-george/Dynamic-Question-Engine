from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class Category(Base):
    __tablename__ = "categories"

    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    mappings = relationship("CategoryQuestionMapping", back_populates="category")
    sessions = relationship("AssessmentSession", back_populates="category")

# Import related classes at bottom to avoid circular import issues and allow relationship evaluation
from app.models.mapping import CategoryQuestionMapping  # noqa: F401
from app.models.session import AssessmentSession  # noqa: F401
