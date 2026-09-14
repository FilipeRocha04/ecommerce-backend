from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models._helpers import (
    DateTimeType,
    UUIDType,
    atualizado_em_coluna,
    criado_em_coluna,
    id_coluna,
)

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Endereco(Base):
    __tablename__ = "enderecos"

    id: Mapped[UUIDType] = id_coluna()
    usuario_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    logradouro: Mapped[str] = mapped_column(String(200), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    principal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    usuario: Mapped["Usuario"] = relationship(back_populates="enderecos")
