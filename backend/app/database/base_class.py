import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, UUID, MetaData
from sqlalchemy.orm import as_declarative, declared_attr

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention)

@as_declarative(metadata=metadata)
class Base:
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL", use_alter=True), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL", use_alter=True), nullable=True)
    
    is_deleted = Column(Boolean, default=False, index=True, nullable=False)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
