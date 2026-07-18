from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    
    district_code = Column(String(10), nullable=False)
    area_code = Column(String(10), nullable=False)
    category_code = Column(String(10), nullable=False)
    running_number = Column(Integer, nullable=False)
    registration_number = Column(String(50), unique=True, index=True, nullable=False)

    user = relationship("User", back_populates="profile", foreign_keys=[user_id])
