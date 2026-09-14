import uuid

from pydantic import BaseModel


class CompatibilidadeResposta(BaseModel):
    compativel: bool
    produto_id: uuid.UUID
    variante_veiculo_id: uuid.UUID
