from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Answer(Base):
    __tablename__ = "answers"

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    answer_text = Column(
        String(255),
        nullable=False
    )

    display_order = Column(
        Integer,
        default=0,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # NEW FIELD
    

    question = relationship(
        "Question",
        foreign_keys=[question_id],
        back_populates="answers"
    )

   

    responses = relationship(
        "UserResponse",
        back_populates="answer"
    )


from app.models.question import Question
from app.models.response import UserResponse