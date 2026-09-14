import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import RecursoNaoEncontrado
from app.models.veiculo import FabricanteVeiculo, ModeloVeiculo, VarianteVeiculo
from app.repositories.veiculo import VeiculoRepository


class VeiculoService:
    def __init__(self, db: Session):
        self.repository = VeiculoRepository(db)

    def listar_fabricantes(self) -> list[FabricanteVeiculo]:
        return self.repository.listar_fabricantes()

    def obter_fabricante(self, fabricante_id: uuid.UUID) -> FabricanteVeiculo:
        fabricante = self.repository.obter_fabricante(fabricante_id)
        if fabricante is None:
            raise RecursoNaoEncontrado(
                "Fabricante não encontrado.", codigo="fabricante_nao_encontrado"
            )
        return fabricante

    def listar_modelos(self, *, fabricante_id: uuid.UUID | None = None) -> list[ModeloVeiculo]:
        return self.repository.listar_modelos(fabricante_id=fabricante_id)

    def obter_modelo(self, modelo_id: uuid.UUID) -> ModeloVeiculo:
        modelo = self.repository.obter_modelo(modelo_id)
        if modelo is None:
            raise RecursoNaoEncontrado("Modelo não encontrado.", codigo="modelo_nao_encontrado")
        return modelo

    def listar_variantes(
        self,
        *,
        fabricante: str | None = None,
        modelo: str | None = None,
        ano: int | None = None,
        motor: str | None = None,
    ) -> list[VarianteVeiculo]:
        return self.repository.listar_variantes(
            fabricante_nome=fabricante, modelo_nome=modelo, ano=ano, motor=motor
        )

    def obter_variante(self, variante_id: uuid.UUID) -> VarianteVeiculo:
        variante = self.repository.obter_variante(variante_id)
        if variante is None:
            raise RecursoNaoEncontrado("Variante não encontrada.", codigo="variante_nao_encontrada")
        return variante
