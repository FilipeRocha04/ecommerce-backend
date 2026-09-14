import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import RecursoNaoEncontrado
from app.models.marca import Marca
from app.repositories.marca import MarcaRepository


class MarcaService:
    def __init__(self, db: Session):
        self.repository = MarcaRepository(db)

    def listar(self, *, pagina: int, tamanho_pagina: int) -> tuple[list[Marca], int]:
        offset = (pagina - 1) * tamanho_pagina
        return self.repository.listar(offset=offset, limite=tamanho_pagina)

    def obter_por_id(self, marca_id: uuid.UUID) -> Marca:
        marca = self.repository.obter_por_id(marca_id)
        if marca is None:
            raise RecursoNaoEncontrado("Marca não encontrada.", codigo="marca_nao_encontrada")
        return marca
