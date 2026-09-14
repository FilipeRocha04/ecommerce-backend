import uuid

from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.schemas.veiculo import (
    FabricanteVeiculoResposta,
    ModeloVeiculoResposta,
    VarianteVeiculoResposta,
)
from app.services.veiculo import VeiculoService

router = APIRouter(prefix="/api/v1/veiculos", tags=["Veículos"])


@router.get("/fabricantes", response_model=list[FabricanteVeiculoResposta])
def listar_fabricantes(db: DbSession) -> list[FabricanteVeiculoResposta]:
    service = VeiculoService(db)
    return service.listar_fabricantes()


@router.get("/fabricantes/{fabricante_id}", response_model=FabricanteVeiculoResposta)
def obter_fabricante(fabricante_id: uuid.UUID, db: DbSession) -> FabricanteVeiculoResposta:
    service = VeiculoService(db)
    return service.obter_fabricante(fabricante_id)


@router.get("/modelos", response_model=list[ModeloVeiculoResposta])
def listar_modelos(
    db: DbSession, fabricante_id: uuid.UUID | None = None
) -> list[ModeloVeiculoResposta]:
    service = VeiculoService(db)
    return service.listar_modelos(fabricante_id=fabricante_id)


@router.get("/modelos/{modelo_id}", response_model=ModeloVeiculoResposta)
def obter_modelo(modelo_id: uuid.UUID, db: DbSession) -> ModeloVeiculoResposta:
    service = VeiculoService(db)
    return service.obter_modelo(modelo_id)


@router.get("/variantes", response_model=list[VarianteVeiculoResposta])
def listar_variantes(
    db: DbSession,
    fabricante: str | None = Query(default=None),
    modelo: str | None = Query(default=None),
    ano: int | None = Query(default=None),
    motor: str | None = Query(default=None),
) -> list[VarianteVeiculoResposta]:
    service = VeiculoService(db)
    return service.listar_variantes(fabricante=fabricante, modelo=modelo, ano=ano, motor=motor)


@router.get("/variantes/{variante_id}", response_model=VarianteVeiculoResposta)
def obter_variante(variante_id: uuid.UUID, db: DbSession) -> VarianteVeiculoResposta:
    service = VeiculoService(db)
    return service.obter_variante(variante_id)
