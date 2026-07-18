from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.question import QuestionResponse

class AssessmentStartRequest(BaseModel):
    category_id: int

class SubmitAnswerRequest(BaseModel):
    session_id: int
    question_id: int
    answer_id: int

class SubmitAnswerResponse(BaseModel):
    success: bool
    is_completed: bool
    progress_percentage: float
    next_question: Optional[QuestionResponse] = None

class AssessmentSessionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    current_question_index: int
    current_question_id: Optional[int] = None
    status: str
    start_time: datetime
    completion_time: Optional[datetime] = None
    progress_percentage: float

    class Config:
        from_attributes = True

class UserResponseItem(BaseModel):
    id: int
    session_id: int
    question_id: int
    question_text: str
    answer_id: int
    answer_text: str
    timestamp: datetime

    class Config:
        from_attributes = True

class AssessmentHistoryItem(BaseModel):
    session: AssessmentSessionResponse
    category_name: str
    responses: List[UserResponseItem] = []

    class Config:
        from_attributes = True
