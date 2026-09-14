from decimal import Decimal
from typing import Any

from sqlalchemy import Enum, ForeignKey, Integer, String
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
from app.models.enums import Canal, StatusPedido


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[UUIDType] = id_coluna()
    numero_pedido: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    usuario_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status: Mapped[StatusPedido] = mapped_column(
        Enum(StatusPedido, name="status_pedido", native_enum=True),
        nullable=False,
        default=StatusPedido.AGUARDANDO_PAGAMENTO,
        index=True,
    )
    subtotal: Mapped[Decimal] = dinheiro_coluna()
    desconto: Mapped[Decimal] = dinheiro_coluna()
    frete: Mapped[Decimal] = dinheiro_coluna()
    total: Mapped[Decimal] = dinheiro_coluna()
    canal: Mapped[Canal] = mapped_column(
        Enum(Canal, name="canal", native_enum=True),
        nullable=False,
        default=Canal.WEB,
    )
    endereco_entrega: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[UUIDType] = id_coluna()
    pedido_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    produto_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sku: Mapped[str] = mapped_column(String(60), nullable=False)
    nome_produto: Mapped[str] = mapped_column(String(200), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[Decimal] = dinheiro_coluna()
    total: Mapped[Decimal] = dinheiro_coluna()

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
