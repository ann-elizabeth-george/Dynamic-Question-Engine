from sqlalchemy import Column, String
from app.database.base_class import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"

    config_key = Column(String(100), unique=True, index=True, nullable=False)
    config_value = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
