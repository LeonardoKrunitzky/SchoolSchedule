from sqlalchemy import Column, ForeignKey, Date, Time, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class ActivityHour(Base):
    """
    Entity representing a generated activity-hour occurrence tied to a fixed availability slot.
    """
    __tablename__ = "activity_hour"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fixed_availability_id = Column(UUID(as_uuid=True), ForeignKey("fixed_availability.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False, default="GENERATED")
