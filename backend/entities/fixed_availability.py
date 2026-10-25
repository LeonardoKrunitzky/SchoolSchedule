from sqlalchemy import Column, String, SmallInteger, Time, ForeignKey, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class FixedAvailability(Base):
    """
    Entity representing a user's fixed weekly availability for a class.
    """
    __tablename__ = "fixed_availability"
    __table_args__ = (CheckConstraint("weekday BETWEEN 1 AND 7", name="ck_fixed_availability_weekday"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    weekday = Column(SmallInteger, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    observacao = Column(String(255), nullable=True)
