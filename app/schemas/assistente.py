import uuid
from typing import Literal

from pydantic import BaseModel

from app.schemas.carrinho import CarrinhoResposta
from app.schemas.produto import ProdutoResposta


class MensagemChat(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AssistenteConversarRequest(BaseModel):
    mensagem: str
    historico: list[MensagemChat] = []
    carrinho_id: uuid.UUID | None = None
    variante_veiculo_id: uuid.UUID | None = None


class AssistenteConversarResposta(BaseModel):
    resposta: str
    produtos: list[ProdutoResposta] = []
    carrinho: CarrinhoResposta | None = None
