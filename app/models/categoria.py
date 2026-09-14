from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models._helpers import (
    DateTimeType,
    UUIDType,
    atualizado_em_coluna,
    criado_em_coluna,
    id_coluna,
)

if TYPE_CHECKING:
    from app.models.produto import Produto


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[UUIDType] = id_coluna()
    categoria_pai_id: Mapped[UUIDType | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categorias.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    created_at: Mapped[DateTimeType] = criado_em_coluna()
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    categoria_pai: Mapped["Categoria | None"] = relationship(
        remote_side="Categoria.id", back_populates="subcategorias"
    )
    subcategorias: Mapped[list["Categoria"]] = relationship(back_populates="categoria_pai")
    produtos: Mapped[list["Produto"]] = relationship(back_populates="categoria")
