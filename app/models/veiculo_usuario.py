from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, SmallInteger, String
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
    from app.models.veiculo import VarianteVeiculo


class VeiculoUsuario(Base):
    __tablename__ = "veiculos_usuarios"

    id: Mapped[UUIDType] = id_coluna()
    usuario_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    variante_veiculo_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("variantes_veiculos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    ano: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    apelido: Mapped[str | None] = mapped_column(String(80), nullable=True)
    placa: Mapped[str | None] = mapped_column(String(10), nullable=True)
    principal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    usuario: Mapped["Usuario"] = relationship(back_populates="veiculos")
    variante: Mapped["VarianteVeiculo"] = relationship(back_populates="veiculos_usuarios")
