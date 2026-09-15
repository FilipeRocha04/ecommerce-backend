import uuid
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.orm import Session

from app.agent.graph import criar_agente
from app.agent.tools import criar_tools
from app.core.config import get_settings
from app.core.exceptions import DadosInvalidos
from app.models.produto import Produto
from app.schemas.assistente import MensagemChat
from app.services.carrinho import CarrinhoService


class AssistenteService:
    def __init__(self, db: Session):
        self.db = db

    def conversar(
        self,
        mensagem: str,
        historico: list[MensagemChat],
        carrinho_id: uuid.UUID | None,
        variante_veiculo_id: uuid.UUID | None,
    ) -> tuple[str, list[Produto], Any]:
        settings = get_settings()
        if not settings.openai_api_key:
            raise DadosInvalidos(
                "Assistente de IA não configurado: defina OPENAI_API_KEY no backend.",
                codigo="assistente_nao_configurado",
            )

        contexto: dict[str, Any] = {
            "produtos": {},
            "carrinho_id": str(carrinho_id) if carrinho_id else None,
        }
        tools = criar_tools(self.db, contexto)
        agente = criar_agente(tools)

        mensagens: list[Any] = [
            HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
            for m in historico
        ]

        contexto_extra = []
        if variante_veiculo_id:
            contexto_extra.append(
                f"variante_veiculo_id do veículo selecionado: {variante_veiculo_id}"
            )
        if contexto["carrinho_id"]:
            contexto_extra.append(f"carrinho_id atual: {contexto['carrinho_id']}")
        texto_usuario = mensagem
        if contexto_extra:
            texto_usuario += "\n\n[" + "; ".join(contexto_extra) + "]"
        mensagens.append(HumanMessage(content=texto_usuario))

        resultado = agente.invoke({"messages": mensagens})
        resposta = resultado["messages"][-1].content

        produtos = list(contexto["produtos"].values())

        carrinho = None
        if contexto["carrinho_id"]:
            carrinho = CarrinhoService(self.db).obter_por_id(uuid.UUID(contexto["carrinho_id"]))

        return resposta, produtos, carrinho
