import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import RecursoNaoEncontrado
from app.models.estoque import Estoque
from app.repositories.estoque import EstoqueRepository
from app.services.produto import ProdutoService


class EstoqueService:
    def __init__(self, db: Session):
        self.repository = EstoqueRepository(db)
        self.produto_service = ProdutoService(db)

    def obter_por_produto(self, produto_id: uuid.UUID) -> Estoque:
        self.produto_service.obter_por_id(produto_id)
        estoque = self.repository.obter_por_produto(produto_id)
        if estoque is None:
            raise RecursoNaoEncontrado(
                "Estoque não encontrado para o produto.", codigo="estoque_nao_encontrado"
            )
        return estoque
