import uuid

from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.schemas.marca import MarcaResposta
from app.schemas.paginacao import Pagina
from app.services.marca import MarcaService

router = APIRouter(prefix="/api/v1/marcas", tags=["Marcas"])


@router.get("", response_model=Pagina[MarcaResposta])
def listar_marcas(
    db: DbSession,
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=20, ge=1, le=100),
) -> Pagina[MarcaResposta]:
    service = MarcaService(db)
    itens, total = service.listar(pagina=pagina, tamanho_pagina=tamanho_pagina)
    return Pagina.criar(itens, total, pagina, tamanho_pagina)


@router.get("/{marca_id}", response_model=MarcaResposta)
def obter_marca(marca_id: uuid.UUID, db: DbSession) -> MarcaResposta:
    service = MarcaService(db)
    return service.obter_por_id(marca_id)
