from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_db
from app.schemas.district import DistrictResponse
from app.services import district_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[DistrictResponse]
)
def get_districts(
    db: Session = Depends(get_db)
):
    return district_service.get_all_districts(db)