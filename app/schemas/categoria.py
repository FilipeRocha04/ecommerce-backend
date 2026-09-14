import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoriaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    categoria_pai_id: uuid.UUID | None
    nome: str
    slug: str
    created_at: datetime
    updated_at: datetime


class CategoriaComSubcategorias(CategoriaResposta):
    subcategorias: list["CategoriaResposta"] = []
