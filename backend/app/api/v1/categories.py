from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.auth import get_db, require_admin, get_current_active_user
from app.schemas.category import CategoryCreate, CategoryResponse, MappingCreate, MappingResponse
from app.services import category_service

router = APIRouter()

@router.get("", response_model=List[CategoryResponse])
def read_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return category_service.get_active_categories(db)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return category_service.create_category(db, category_in)

@router.post("/map", response_model=MappingResponse, status_code=status.HTTP_201_CREATED)
def map_question_to_category(
    mapping_in: MappingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return category_service.create_mapping(db, mapping_in)
