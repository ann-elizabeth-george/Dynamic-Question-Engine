from pydantic import BaseModel
from typing import List, Optional

class AnswerCreate(BaseModel):
    answer_text: str
    display_order: int
    is_active: Optional[bool] = True

class AnswerResponse(BaseModel):
    id: int
    question_id: int
    answer_text: str
    display_order: int
    is_active: bool

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    code: str
    question_text: str
    question_type: str = "SINGLE_CHOICE" # e.g. SINGLE_CHOICE, MULTI_CHOICE
    status: str = "ACTIVE"
    answers: List[AnswerCreate] = []

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    status: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    code: str
    question_text: str
    question_type: str
    status: str
    answers: List[AnswerResponse] = []

    class Config:
        from_attributes = True
