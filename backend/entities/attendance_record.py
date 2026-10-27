from sqlalchemy import Column, String, Date, Numeric, ForeignKey, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class AttendanceRecord(Base):
    """
    Entity representing an absence or overtime record for a user.
    """
    __tablename__ = "attendance_record"
    __table_args__ = (CheckConstraint("type IN ('ABSENCE', 'OVERTIME')", name="ck_attendance_record_type"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(20), nullable=False)
    hours = Column(Numeric(5, 2), nullable=True)
    notes = Column(String(255), nullable=True)
