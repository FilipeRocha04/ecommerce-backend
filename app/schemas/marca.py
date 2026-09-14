import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MarcaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    slug: str
    created_at: datetime
