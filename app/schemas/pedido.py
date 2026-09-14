import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.enums import Canal, StatusPedido


class PedidoCriar(BaseModel):
    usuario_id: uuid.UUID
    carrinho_id: uuid.UUID
    endereco_entrega: dict[str, Any]


class ItemPedidoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    produto_id: uuid.UUID
    sku: str
    nome_produto: str
    quantidade: int
    preco_unitario: Decimal
    total: Decimal


class PedidoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    numero_pedido: str
    usuario_id: uuid.UUID
    status: StatusPedido
    subtotal: Decimal
    desconto: Decimal
    frete: Decimal
    total: Decimal
    canal: Canal
    endereco_entrega: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    itens: list[ItemPedidoResposta] = []
