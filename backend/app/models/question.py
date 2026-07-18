from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Question(Base):
    __tablename__ = "questions"

    code = Column(String(50), unique=True, index=True, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(
        String(50),
        default="SINGLE_CHOICE",
        nullable=False
    )
    status = Column(
        String(50),
        default="ACTIVE",
        nullable=False
    )

    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    mappings = relationship(
        "CategoryQuestionMapping",
        back_populates="question"
    )

    responses = relationship(
        "UserResponse",
        back_populates="question"
    )


from app.models.answer import Answer
from app.models.mapping import CategoryQuestionMapping
from app.models.response import UserResponse