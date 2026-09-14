import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.compatibilidade import CompatibilidadeProdutoVeiculo


class CompatibilidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe(self, produto_id: uuid.UUID, variante_veiculo_id: uuid.UUID) -> bool:
        query = select(CompatibilidadeProdutoVeiculo.id).where(
            CompatibilidadeProdutoVeiculo.produto_id == produto_id,
            CompatibilidadeProdutoVeiculo.variante_veiculo_id == variante_veiculo_id,
        )
        return self.db.scalar(query) is not None
