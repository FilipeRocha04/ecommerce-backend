import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FabricanteVeiculoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    created_at: datetime


class ModeloVeiculoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    fabricante_id: uuid.UUID
    nome: str
    created_at: datetime


class VarianteVeiculoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    modelo_id: uuid.UUID
    fabricante_nome: str
    modelo_nome: str
    ano_inicio: int
    ano_fim: int
    motor: str
    versao: str | None
    combustivel: str
    cambio: str
    created_at: datetime
    updated_at: datetime
