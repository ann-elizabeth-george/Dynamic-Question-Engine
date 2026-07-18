from sqlalchemy import Column, String, DateTime, JSON
from app.database.base_class import Base

class EventOutbox(Base):
    __tablename__ = "event_outbox"

    event_name = Column(String(100), nullable=False)
    event_data = Column(JSON, nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)
    processed_at = Column(DateTime, nullable=True)
