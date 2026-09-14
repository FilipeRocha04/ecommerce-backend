from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models._helpers import (
    DateTimeType,
    UUIDType,
    atualizado_em_coluna,
    criado_em_coluna,
    dinheiro_coluna,
    id_coluna,
)

if TYPE_CHECKING:
    from app.models.categoria import Categoria
    from app.models.compatibilidade import CompatibilidadeProdutoVeiculo
    from app.models.estoque import Estoque
    from app.models.marca import Marca


class Produto(Base):
    __tablename__ = "produtos"
    __table_args__ = (
        CheckConstraint("preco >= 0", name="produtos_preco_positivo_check"),
        CheckConstraint(
            "preco_promocional IS NULL OR preco_promocional < preco",
            name="produtos_preco_promocional_menor_check",
        ),
        CheckConstraint("meses_garantia >= 0", name="produtos_meses_garantia_check"),
    )

    id: Mapped[UUIDType] = id_coluna()
    sku: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    marca_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), ForeignKey("marcas.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    categoria_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categorias.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False, default="")
    codigo_peca: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    preco: Mapped[Decimal] = dinheiro_coluna()
    preco_promocional: Mapped[Decimal | None] = dinheiro_coluna(nullable=True)
    meses_garantia: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    marca: Mapped["Marca"] = relationship(back_populates="produtos")
    categoria: Mapped["Categoria"] = relationship(back_populates="produtos")
    imagens: Mapped[list["ImagemProduto"]] = relationship(
        back_populates="produto", cascade="all, delete-orphan", order_by="ImagemProduto.posicao"
    )
    especificacao: Mapped["EspecificacaoProduto | None"] = relationship(
        back_populates="produto", cascade="all, delete-orphan", uselist=False
    )
    estoque: Mapped["Estoque | None"] = relationship(
        back_populates="produto", cascade="all, delete-orphan", uselist=False
    )
    compatibilidades: Mapped[list["CompatibilidadeProdutoVeiculo"]] = relationship(
        back_populates="produto", cascade="all, delete-orphan"
    )


class ImagemProduto(Base):
    __tablename__ = "imagens_produtos"

    id: Mapped[UUIDType] = id_coluna()
    produto_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    posicao: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    created_at: Mapped[DateTimeType] = criado_em_coluna()

    produto: Mapped["Produto"] = relationship(back_populates="imagens")


class EspecificacaoProduto(Base):
    __tablename__ = "especificacoes_produtos"

    id: Mapped[UUIDType] = id_coluna()
    produto_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    especificacoes: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    produto: Mapped["Produto"] = relationship(back_populates="especificacao")
