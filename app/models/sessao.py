from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models._helpers import DateTimeType, UUIDType, id_coluna
from app.models.enums import Canal


class Sessao(Base):
    __tablename__ = "sessoes"

    id: Mapped[UUIDType] = id_coluna()
    usuario_id: Mapped[UUIDType | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    iniciada_em: Mapped[DateTimeType] = mapped_column(DateTime(timezone=True), nullable=False)
    finalizada_em: Mapped[DateTimeType | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    canal_inicial: Mapped[Canal] = mapped_column(
        Enum(Canal, name="canal", native_enum=True), nullable=False
    )
