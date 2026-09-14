from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
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
from app.models.enums import Canal, StatusCarrinho

if TYPE_CHECKING:
    from app.models.produto import Produto


class Carrinho(Base):
    __tablename__ = "carrinhos"

    id: Mapped[UUIDType] = id_coluna()
    usuario_id: Mapped[UUIDType | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=True, index=True
    )
    sessao_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    status: Mapped[StatusCarrinho] = mapped_column(
        Enum(StatusCarrinho, name="status_carrinho", native_enum=True),
        nullable=False,
        default=StatusCarrinho.ATIVO,
    )
    canal: Mapped[Canal] = mapped_column(
        Enum(Canal, name="canal", native_enum=True), nullable=False, default=Canal.WEB
    )
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    itens: Mapped[list["ItemCarrinho"]] = relationship(
        back_populates="carrinho", cascade="all, delete-orphan"
    )


class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"
    __table_args__ = (
        UniqueConstraint(
            "carrinho_id", "produto_id", name="itens_carrinho_carrinho_produto_unique"
        ),
        CheckConstraint("quantidade > 0", name="itens_carrinho_quantidade_positiva_check"),
    )

    id: Mapped[UUIDType] = id_coluna()
    carrinho_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("carrinhos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    produto_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    preco_unitario: Mapped[Decimal] = dinheiro_coluna()
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    carrinho: Mapped["Carrinho"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship()
