import uuid

from sqlalchemy.orm import Session

from app.repositories.compatibilidade import CompatibilidadeRepository
from app.services.produto import ProdutoService
from app.services.veiculo import VeiculoService


class CompatibilidadeService:
    def __init__(self, db: Session):
        self.repository = CompatibilidadeRepository(db)
        self.produto_service = ProdutoService(db)
        self.veiculo_service = VeiculoService(db)

    def verificar(self, produto_id: uuid.UUID, variante_veiculo_id: uuid.UUID) -> bool:
        self.produto_service.obter_por_id(produto_id)
        self.veiculo_service.obter_variante(variante_veiculo_id)
        return self.repository.existe(produto_id, variante_veiculo_id)
