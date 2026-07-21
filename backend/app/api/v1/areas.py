from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db
from app.models.area import Area
from app.schemas.area import AreaResponse

router = APIRouter()


@router.get("/{district_id}", response_model=list[AreaResponse])
def get_areas(district_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Area)
        .filter(Area.district_id == district_id)
        .order_by(Area.name)
        .all()
    )