from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class SchoolClass(Base):
    """
    Entity representing a class (turma) in the database.
    """
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    name = Column(String(50), nullable=False)
