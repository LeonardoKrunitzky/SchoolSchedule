from sqlalchemy import Column, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class SubstituteSchedule(Base):
    """
    Entity representing a substitution assignment for a professional in a class.
    """
    __tablename__ = "substitute_schedule"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
