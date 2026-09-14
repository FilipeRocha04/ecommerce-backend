from typing import TYPE_CHECKING

from sqlalchemy import String
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
    from app.models.endereco import Endereco
    from app.models.veiculo_usuario import VeiculoUsuario


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[UUIDType] = id_coluna()
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True, index=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    enderecos: Mapped[list["Endereco"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )
    veiculos: Mapped[list["VeiculoUsuario"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )
