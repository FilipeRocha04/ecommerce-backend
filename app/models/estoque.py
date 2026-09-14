from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models._helpers import DateTimeType, UUIDType, atualizado_em_coluna, id_coluna

if TYPE_CHECKING:
    from app.models.produto import Produto


class Estoque(Base):
    __tablename__ = "estoques"
    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="estoques_quantidade_positiva_check"),
        CheckConstraint(
            "quantidade_reservada >= 0", name="estoques_quantidade_reservada_positiva_check"
        ),
        CheckConstraint(
            "quantidade_reservada <= quantidade", name="estoques_reservada_menor_quantidade_check"
        ),
    )

    id: Mapped[UUIDType] = id_coluna()
    produto_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quantidade_reservada: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[DateTimeType] = atualizado_em_coluna()

    produto: Mapped["Produto"] = relationship(back_populates="estoque")

    @property
    def quantidade_disponivel(self) -> int:
        return self.quantidade - self.quantidade_reservada
