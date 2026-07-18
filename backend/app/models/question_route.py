from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class QuestionRoute(Base):
    __tablename__ = "question_routes"

    answer_id = Column(
        Integer,
        ForeignKey("answers.id"),
        nullable=False
    )

    next_question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    answer = relationship("Answer")

    next_question = relationship(
        "Question",
        foreign_keys=[next_question_id]
    )