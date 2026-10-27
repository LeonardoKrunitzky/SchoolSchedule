from sqlalchemy import Column, ForeignKey, DateTime, String, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class Horario(Base):
    """
    Entity representing a scheduled slot: either a generated activity hour tied to a
    fixed availability, or a substitution assignment.
    """
    __tablename__ = "horario"
    __table_args__ = (
        CheckConstraint("tipo IN ('ACTIVITY_HOUR', 'SUBSTITUTE')", name="horario_tipo_check"),
        CheckConstraint("end_datetime > start_datetime", name="horario_datetime_check"),
        CheckConstraint("tipo = 'SUBSTITUTE' OR fixed_availability_id IS NOT NULL", name="horario_fixed_availability_check"),
        Index("idx_horario_user_start", "user_id", "start_datetime"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tipo = Column(String(20), nullable=False, default="ACTIVITY_HOUR")
    fixed_availability_id = Column(UUID(as_uuid=True), ForeignKey("fixed_availability.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="GENERATED")
    observacao = Column(String(255), nullable=True)
