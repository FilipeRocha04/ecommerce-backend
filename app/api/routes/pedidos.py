import uuid

from fastapi import APIRouter, Query, status

from app.api.deps import DbSession
from app.schemas.paginacao import Pagina
from app.schemas.pedido import PedidoCriar, PedidoResposta
from app.services.pedido import PedidoService

router = APIRouter(prefix="/api/v1/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoResposta, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCriar, db: DbSession) -> PedidoResposta:
    service = PedidoService(db)
    return service.criar(
        usuario_id=dados.usuario_id,
        carrinho_id=dados.carrinho_id,
        endereco_entrega=dados.endereco_entrega,
    )


@router.get("", response_model=Pagina[PedidoResposta])
def listar_pedidos(
    db: DbSession,
    usuario_id: uuid.UUID,
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=20, ge=1, le=100),
) -> Pagina[PedidoResposta]:
    service = PedidoService(db)
    itens, total = service.listar_por_usuario(
        usuario_id, pagina=pagina, tamanho_pagina=tamanho_pagina
    )
    return Pagina.criar(itens, total, pagina, tamanho_pagina)


@router.get("/{pedido_id}", response_model=PedidoResposta)
def obter_pedido(pedido_id: uuid.UUID, db: DbSession) -> PedidoResposta:
    service = PedidoService(db)
    return service.obter_por_id(pedido_id)
