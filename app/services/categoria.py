import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import RecursoNaoEncontrado
from app.models.categoria import Categoria
from app.repositories.categoria import CategoriaRepository


class CategoriaService:
    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def listar(self) -> list[Categoria]:
        return self.repository.listar()

    def obter_por_id(self, categoria_id: uuid.UUID) -> Categoria:
        categoria = self.repository.obter_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado(
                "Categoria não encontrada.", codigo="categoria_nao_encontrada"
            )
        return categoria
