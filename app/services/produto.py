import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import RecursoNaoEncontrado
from app.models.produto import Produto
from app.repositories.produto import FiltrosProduto, ProdutoRepository


class ProdutoService:
    def __init__(self, db: Session):
        self.repository = ProdutoRepository(db)

    def listar(
        self,
        *,
        pagina: int,
        tamanho_pagina: int,
        categoria_id: uuid.UUID | None = None,
        marca_id: uuid.UUID | None = None,
        preco_minimo: Decimal | None = None,
        preco_maximo: Decimal | None = None,
        variante_veiculo_id: uuid.UUID | None = None,
    ) -> tuple[list[Produto], int]:
        filtros = FiltrosProduto(
            categoria_id=categoria_id,
            marca_id=marca_id,
            preco_minimo=preco_minimo,
            preco_maximo=preco_maximo,
            variante_veiculo_id=variante_veiculo_id,
        )
        offset = (pagina - 1) * tamanho_pagina
        return self.repository.listar(filtros, offset=offset, limite=tamanho_pagina)

    def buscar(self, termo: str, *, pagina: int, tamanho_pagina: int) -> tuple[list[Produto], int]:
        filtros = FiltrosProduto(termo_busca=termo)
        offset = (pagina - 1) * tamanho_pagina
        return self.repository.listar(filtros, offset=offset, limite=tamanho_pagina)

    def obter_por_id(self, produto_id: uuid.UUID) -> Produto:
        produto = self.repository.obter_por_id(produto_id)
        if produto is None:
            raise RecursoNaoEncontrado("Produto não encontrado.", codigo="produto_nao_encontrado")
        return produto
