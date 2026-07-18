from sqlalchemy import Column, String, Integer, UniqueConstraint
from app.database.base_class import Base

class RegistrationCounter(Base):
    __tablename__ = "registration_counters"

    district_code = Column(String(10), nullable=False)
    area_code = Column(String(10), nullable=False)
    category_code = Column(String(10), nullable=False)
    current_number = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        UniqueConstraint('district_code', 'area_code', 'category_code', name='_district_area_category_uc'),
    )
