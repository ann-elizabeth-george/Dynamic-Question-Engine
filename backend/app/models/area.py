from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)

    district_id = Column(
        Integer,
        ForeignKey("districts.id"),
        nullable=False
    )

    name = Column(String(150), nullable=False)

    code = Column(String(3), nullable=False)

    district = relationship("District", back_populates="areas")