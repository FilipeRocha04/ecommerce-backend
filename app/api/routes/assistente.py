from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas.assistente import AssistenteConversarRequest, AssistenteConversarResposta
from app.services.assistente import AssistenteService

router = APIRouter(prefix="/api/v1/assistente", tags=["Assistente"])


@router.post("/conversar", response_model=AssistenteConversarResposta)
def conversar(dados: AssistenteConversarRequest, db: DbSession) -> AssistenteConversarResposta:
    service = AssistenteService(db)
    resposta, produtos, carrinho = service.conversar(
        dados.mensagem, dados.historico, dados.carrinho_id, dados.variante_veiculo_id
    )
    return AssistenteConversarResposta(resposta=resposta, produtos=produtos, carrinho=carrinho)
