from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models._helpers import DateTimeType, UUIDType, criado_em_coluna, id_coluna

if TYPE_CHECKING:
    from app.models.produto import Produto


class Marca(Base):
    __tablename__ = "marcas"

    id: Mapped[UUIDType] = id_coluna()
    nome: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    created_at: Mapped[DateTimeType] = criado_em_coluna()

    produtos: Mapped[list["Produto"]] = relationship(back_populates="marca")
