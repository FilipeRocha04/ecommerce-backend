import uuid

from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas.categoria import CategoriaResposta
from app.services.categoria import CategoriaService

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorias"])


@router.get("", response_model=list[CategoriaResposta])
def listar_categorias(db: DbSession) -> list[CategoriaResposta]:
    service = CategoriaService(db)
    return service.listar()


@router.get("/{categoria_id}", response_model=CategoriaResposta)
def obter_categoria(categoria_id: uuid.UUID, db: DbSession) -> CategoriaResposta:
    service = CategoriaService(db)
    return service.obter_por_id(categoria_id)
