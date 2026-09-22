from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class Class(Base):
    """
    Entity representing a school class in the database.
    """
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), nullable=False)
