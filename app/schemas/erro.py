from pydantic import BaseModel


class ErroResposta(BaseModel):
    erro: str
    mensagem: str
