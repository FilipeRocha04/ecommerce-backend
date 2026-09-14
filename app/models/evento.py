from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models._helpers import UUIDType, id_coluna
from app.models.enums import Canal


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[UUIDType] = id_coluna()
    nome_evento: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    timestamp: Mapped[Any] = mapped_column(DateTime(timezone=True), nullable=False)
    sessao_id: Mapped[UUIDType | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessoes.id", ondelete="SET NULL"), nullable=True, index=True
    )
    usuario_id: Mapped[UUIDType | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    canal: Mapped[Canal] = mapped_column(
        Enum(Canal, name="canal", native_enum=True), nullable=False
    )
    propriedades: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
