import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.veiculo import FabricanteVeiculo, ModeloVeiculo, VarianteVeiculo


class VeiculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_fabricantes(self) -> list[FabricanteVeiculo]:
        return list(
            self.db.execute(select(FabricanteVeiculo).order_by(FabricanteVeiculo.nome))
            .scalars()
            .all()
        )

    def obter_fabricante(self, fabricante_id: uuid.UUID) -> FabricanteVeiculo | None:
        return self.db.get(FabricanteVeiculo, fabricante_id)

    def listar_modelos(self, *, fabricante_id: uuid.UUID | None = None) -> list[ModeloVeiculo]:
        query = select(ModeloVeiculo).order_by(ModeloVeiculo.nome)
        if fabricante_id is not None:
            query = query.where(ModeloVeiculo.fabricante_id == fabricante_id)
        return list(self.db.execute(query).scalars().all())

    def obter_modelo(self, modelo_id: uuid.UUID) -> ModeloVeiculo | None:
        return self.db.get(ModeloVeiculo, modelo_id)

    def listar_variantes(
        self,
        *,
        fabricante_nome: str | None = None,
        modelo_nome: str | None = None,
        ano: int | None = None,
        motor: str | None = None,
    ) -> list[VarianteVeiculo]:
        query = select(VarianteVeiculo).join(ModeloVeiculo).join(FabricanteVeiculo)

        if fabricante_nome:
            query = query.where(FabricanteVeiculo.nome.ilike(fabricante_nome))
        if modelo_nome:
            query = query.where(ModeloVeiculo.nome.ilike(modelo_nome))
        if ano is not None:
            query = query.where(VarianteVeiculo.ano_inicio <= ano, VarianteVeiculo.ano_fim >= ano)
        if motor:
            query = query.where(VarianteVeiculo.motor.ilike(motor))

        query = query.options(
            joinedload(VarianteVeiculo.modelo).joinedload(ModeloVeiculo.fabricante)
        ).order_by(VarianteVeiculo.ano_inicio)
        return list(self.db.execute(query).unique().scalars().all())

    def obter_variante(self, variante_id: uuid.UUID) -> VarianteVeiculo | None:
        query = (
            select(VarianteVeiculo)
            .where(VarianteVeiculo.id == variante_id)
            .options(joinedload(VarianteVeiculo.modelo).joinedload(ModeloVeiculo.fabricante))
        )
        return self.db.execute(query).unique().scalar_one_or_none()
