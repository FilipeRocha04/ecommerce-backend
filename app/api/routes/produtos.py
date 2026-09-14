import uuid
from decimal import Decimal

from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.schemas.estoque import EstoqueResposta
from app.schemas.paginacao import Pagina
from app.schemas.produto import ProdutoResposta
from app.services.estoque import EstoqueService
from app.services.produto import ProdutoService

router = APIRouter(prefix="/api/v1/produtos", tags=["Produtos"])


@router.get("", response_model=Pagina[ProdutoResposta])
def listar_produtos(
    db: DbSession,
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=20, ge=1, le=100),
    categoria_id: uuid.UUID | None = None,
    marca_id: uuid.UUID | None = None,
    preco_minimo: Decimal | None = None,
    preco_maximo: Decimal | None = None,
    veiculo: uuid.UUID | None = Query(default=None, description="ID da variante do veículo"),
) -> Pagina[ProdutoResposta]:
    service = ProdutoService(db)
    itens, total = service.listar(
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        categoria_id=categoria_id,
        marca_id=marca_id,
        preco_minimo=preco_minimo,
        preco_maximo=preco_maximo,
        variante_veiculo_id=veiculo,
    )
    return Pagina.criar(itens, total, pagina, tamanho_pagina)


@router.get("/buscar", response_model=Pagina[ProdutoResposta])
def buscar_produtos(
    db: DbSession,
    q: str = Query(min_length=1),
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=20, ge=1, le=100),
) -> Pagina[ProdutoResposta]:
    service = ProdutoService(db)
    itens, total = service.buscar(q, pagina=pagina, tamanho_pagina=tamanho_pagina)
    return Pagina.criar(itens, total, pagina, tamanho_pagina)


@router.get("/{produto_id}", response_model=ProdutoResposta)
def obter_produto(produto_id: uuid.UUID, db: DbSession) -> ProdutoResposta:
    service = ProdutoService(db)
    return service.obter_por_id(produto_id)


@router.get("/{produto_id}/estoque", response_model=EstoqueResposta)
def obter_estoque_produto(produto_id: uuid.UUID, db: DbSession) -> EstoqueResposta:
    service = EstoqueService(db)
    estoque = service.obter_por_produto(produto_id)
    return EstoqueResposta(
        produto_id=estoque.produto_id,
        quantidade=estoque.quantidade,
        quantidade_reservada=estoque.quantidade_reservada,
        quantidade_disponivel=estoque.quantidade_disponivel,
    )
