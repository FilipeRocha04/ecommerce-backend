import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.marca import Marca


class MarcaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, *, offset: int, limite: int) -> tuple[list[Marca], int]:
        total = self.db.query(Marca).count()
        itens = (
            self.db.execute(select(Marca).order_by(Marca.nome).offset(offset).limit(limite))
            .scalars()
            .all()
        )
        return list(itens), total

    def obter_por_id(self, marca_id: uuid.UUID) -> Marca | None:
        return self.db.get(Marca, marca_id)
