from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint, Index, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from connections.database import Base

class Horario(Base):
    """
    Entity representing a scheduled slot (activity hour or substitution).
    """
    __tablename__ = "horario"
    __table_args__ = (
        CheckConstraint("tipo IN ('ACTIVITY_HOUR', 'SUBSTITUTE')", name="ck_horario_tipo"),
        CheckConstraint("end_datetime > start_datetime", name="ck_horario_datetime"),
        CheckConstraint("tipo = 'SUBSTITUTE' OR fixed_availability_id IS NOT NULL", name="ck_horario_fixed_availability"),
        Index("idx_horario_user_start", "user_id", "start_datetime"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    tipo = Column(String(20), nullable=False, default="ACTIVITY_HOUR", server_default="ACTIVITY_HOUR")
    fixed_availability_id = Column(UUID(as_uuid=True), ForeignKey("fixed_availability.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="GENERATED", server_default="GENERATED")
    observacao = Column(String(255), nullable=True)
