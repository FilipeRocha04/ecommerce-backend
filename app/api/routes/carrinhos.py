import uuid

from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.schemas.carrinho import (
    CarrinhoCriar,
    CarrinhoResposta,
    ItemCarrinhoAtualizar,
    ItemCarrinhoCriar,
)
from app.services.carrinho import CarrinhoService

router = APIRouter(prefix="/api/v1/carrinhos", tags=["Carrinhos"])


@router.post("", response_model=CarrinhoResposta, status_code=status.HTTP_201_CREATED)
def criar_carrinho(dados: CarrinhoCriar, db: DbSession) -> CarrinhoResposta:
    service = CarrinhoService(db)
    return service.criar(usuario_id=dados.usuario_id, sessao_id=dados.sessao_id, canal=dados.canal)


@router.get("/{carrinho_id}", response_model=CarrinhoResposta)
def obter_carrinho(carrinho_id: uuid.UUID, db: DbSession) -> CarrinhoResposta:
    service = CarrinhoService(db)
    return service.obter_por_id(carrinho_id)


@router.post(
    "/{carrinho_id}/itens", response_model=CarrinhoResposta, status_code=status.HTTP_201_CREATED
)
def adicionar_item_carrinho(
    carrinho_id: uuid.UUID, dados: ItemCarrinhoCriar, db: DbSession
) -> CarrinhoResposta:
    service = CarrinhoService(db)
    return service.adicionar_item(carrinho_id, dados.produto_id, dados.quantidade)


@router.patch("/{carrinho_id}/itens/{item_id}", response_model=CarrinhoResposta)
def atualizar_item_carrinho(
    carrinho_id: uuid.UUID, item_id: uuid.UUID, dados: ItemCarrinhoAtualizar, db: DbSession
) -> CarrinhoResposta:
    service = CarrinhoService(db)
    return service.atualizar_item(carrinho_id, item_id, dados.quantidade)


@router.delete("/{carrinho_id}/itens/{item_id}", response_model=CarrinhoResposta)
def remover_item_carrinho(
    carrinho_id: uuid.UUID, item_id: uuid.UUID, db: DbSession
) -> CarrinhoResposta:
    service = CarrinhoService(db)
    return service.remover_item(carrinho_id, item_id)
