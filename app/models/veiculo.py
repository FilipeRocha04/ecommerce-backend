from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, SmallInteger, String
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
    from app.models.compatibilidade import CompatibilidadeProdutoVeiculo
    from app.models.veiculo_usuario import VeiculoUsuario


class FabricanteVeiculo(Base):
    __tablename__ = "fabricantes_veiculos"

    id: Mapped[UUIDType] = id_coluna()
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[DateTimeType] = criado_em_coluna()

    modelos: Mapped[list["ModeloVeiculo"]] = relationship(
        back_populates="fabricante", cascade="all, delete-orphan"
    )


class ModeloVeiculo(Base):
    __tablename__ = "modelos_veiculos"

    id: Mapped[UUIDType] = id_coluna()
    fabricante_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fabricantes_veiculos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[DateTimeType] = criado_em_coluna()

    fabricante: Mapped["FabricanteVeiculo"] = relationship(back_populates="modelos")
    variantes: Mapped[list["VarianteVeiculo"]] = relationship(
        back_populates="modelo", cascade="all, delete-orphan"
    )


class VarianteVeiculo(Base):
    __tablename__ = "variantes_veiculos"

    id: Mapped[UUIDType] = id_coluna()
    modelo_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modelos_veiculos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ano_inicio: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ano_fim: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    motor: Mapped[str] = mapped_column(String(50), nullable=False)
    versao: Mapped[str | None] = mapped_column(String(100), nullable=True)
    combustivel: Mapped[str] = mapped_column(String(30), nullable=False)
    cambio: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    modelo: Mapped["ModeloVeiculo"] = relationship(back_populates="variantes")
    veiculos_usuarios: Mapped[list["VeiculoUsuario"]] = relationship(back_populates="variante")
    compatibilidades: Mapped[list["CompatibilidadeProdutoVeiculo"]] = relationship(
        back_populates="variante"
    )

    @property
    def modelo_nome(self) -> str:
        return self.modelo.nome

    @property
    def fabricante_nome(self) -> str:
        return self.modelo.fabricante.nome
