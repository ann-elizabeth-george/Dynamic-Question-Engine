from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.auth import get_db, require_admin, get_current_active_user
from app.schemas.question import QuestionCreate, QuestionResponse
from app.services import question_service

router = APIRouter()

@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    question_in: QuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return question_service.create_question(db, question_in)

@router.get("/category/{category_id}", response_model=List[QuestionResponse])
def read_questions_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return question_service.get_questions_by_category(db, category_id=category_id)
