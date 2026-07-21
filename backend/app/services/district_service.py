from sqlalchemy.orm import Session

from app.models.district import District


def get_all_districts(db: Session):
    return (
        db.query(District)
        .order_by(District.code)
        .all()
    )