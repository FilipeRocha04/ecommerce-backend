import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estoque import Estoque


class EstoqueRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter_por_produto(self, produto_id: uuid.UUID) -> Estoque | None:
        query = select(Estoque).where(Estoque.produto_id == produto_id)
        return self.db.execute(query).scalar_one_or_none()
