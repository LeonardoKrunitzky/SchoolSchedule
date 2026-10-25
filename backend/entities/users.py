from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class Role(Base):
    """
    Entity representing a user role in the database.
    """
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    name = Column(String(100), unique=True, nullable=False)

class User(Base):
    """
    Entity representing a user in the database.
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    registration = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    period = Column(String(20), nullable=True)
    workload = Column(Integer, nullable=True)
    status = Column(Boolean, default=True, server_default=text("true"), nullable=False)
