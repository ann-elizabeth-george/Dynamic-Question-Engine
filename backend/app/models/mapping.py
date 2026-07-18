from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class CategoryQuestionMapping(Base):
    __tablename__ = "category_question_mappings"

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    category = relationship("Category", back_populates="mappings")
    question = relationship("Question", back_populates="mappings")

# Import related classes at bottom to avoid circular import issues and allow relationship evaluation
from app.models.category import Category  # noqa: F401
from app.models.question import Question  # noqa: F401
