from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class District(Base):
    __tablename__ = "districts"

    name = Column(String(100), nullable=False, unique=True)

    code = Column(String(2), nullable=False, unique=True)
    areas = relationship(
    "Area",
    back_populates="district",
    cascade="all, delete"
)