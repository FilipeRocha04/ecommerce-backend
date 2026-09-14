import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categoria import Categoria


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Categoria]:
        return list(self.db.execute(select(Categoria).order_by(Categoria.nome)).scalars().all())

    def obter_por_id(self, categoria_id: uuid.UUID) -> Categoria | None:
        return self.db.get(Categoria, categoria_id)
