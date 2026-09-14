import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.schemas.categoria import CategoriaResposta
from app.schemas.marca import MarcaResposta


class ImagemProdutoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    url: str
    posicao: int


class EspecificacaoProdutoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    especificacoes: dict[str, Any]


class ProdutoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sku: str
    nome: str
    slug: str
    preco: Decimal
    preco_promocional: Decimal | None
    marca_id: uuid.UUID
    categoria_id: uuid.UUID
    ativo: bool


class ProdutoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sku: str
    marca_id: uuid.UUID
    categoria_id: uuid.UUID
    marca: MarcaResposta
    categoria: CategoriaResposta
    nome: str
    slug: str
    descricao: str
    codigo_peca: str
    preco: Decimal
    preco_promocional: Decimal | None
    meses_garantia: int
    ativo: bool
    created_at: datetime
    updated_at: datetime
    imagens: list[ImagemProdutoResposta] = []
    especificacao: EspecificacaoProdutoResposta | None = None
