import uuid

from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas.compatibilidade import CompatibilidadeResposta
from app.services.compatibilidade import CompatibilidadeService

router = APIRouter(prefix="/api/v1/compatibilidade", tags=["Compatibilidade"])


@router.get("", response_model=CompatibilidadeResposta)
def verificar_compatibilidade(
    produto_id: uuid.UUID, variante_veiculo_id: uuid.UUID, db: DbSession
) -> CompatibilidadeResposta:
    service = CompatibilidadeService(db)
    compativel = service.verificar(produto_id, variante_veiculo_id)
    return CompatibilidadeResposta(
        compativel=compativel, produto_id=produto_id, variante_veiculo_id=variante_veiculo_id
    )
