import uuid

from pydantic import BaseModel


class EstoqueResposta(BaseModel):
    produto_id: uuid.UUID
    quantidade: int
    quantidade_reservada: int
    quantidade_disponivel: int
