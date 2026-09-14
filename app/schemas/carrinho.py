import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import Canal, StatusCarrinho


class CarrinhoCriar(BaseModel):
    usuario_id: uuid.UUID | None = None
    sessao_id: str | None = None
    canal: Canal = Canal.WEB


class ItemCarrinhoCriar(BaseModel):
    produto_id: uuid.UUID
    quantidade: int = Field(gt=0)


class ItemCarrinhoAtualizar(BaseModel):
    quantidade: int = Field(gt=0)


class ItemCarrinhoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    produto_id: uuid.UUID
    quantidade: int
    preco_unitario: Decimal
    created_at: datetime
    updated_at: datetime


class CarrinhoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    usuario_id: uuid.UUID | None
    sessao_id: str | None
    status: StatusCarrinho
    canal: Canal
    created_at: datetime
    updated_at: datetime
    itens: list[ItemCarrinhoResposta] = []
