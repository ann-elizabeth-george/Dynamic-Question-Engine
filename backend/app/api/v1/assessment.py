from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.auth import get_db, get_current_active_user
from app.schemas.assessment import (
    AssessmentStartRequest,
    AssessmentSessionResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    AssessmentHistoryItem
)
from app.schemas.question import QuestionResponse
from app.services import assessment_service
from app.models.user import User

router = APIRouter()

@router.post("/start", response_model=AssessmentSessionResponse, status_code=status.HTTP_201_CREATED)
def start_assessment_session(
    request: AssessmentStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return assessment_service.start_session(db, user_id=current_user.id, category_id=request.category_id)

@router.get("/question", response_model=QuestionResponse)
def get_current_assessment_question(
    session_id: int = Query(..., description="Active assessment session ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return assessment_service.get_current_question(db, session_id=session_id, user_id=current_user.id)

@router.post("/answer", response_model=SubmitAnswerResponse)
def submit_assessment_answer(
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return assessment_service.submit_answer(db, user_id=current_user.id, request=request)

@router.get("/history", response_model=List[AssessmentHistoryItem])
def read_assessment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return assessment_service.get_user_assessment_history(db, user_id=current_user.id)
