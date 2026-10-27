from sqlalchemy import Column, ForeignKey, SmallInteger, Time, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class FixedAvailability(Base):
    """
    Entity representing a professional's fixed weekly availability for a class.
    """
    __tablename__ = "fixed_availability"
    __table_args__ = (
        CheckConstraint("weekday BETWEEN 1 AND 7", name="fixed_availability_weekday_check"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    weekday = Column(SmallInteger, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    observacao = Column(String(255), nullable=True)
