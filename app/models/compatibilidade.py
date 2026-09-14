from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models._helpers import DateTimeType, UUIDType, criado_em_coluna, id_coluna

if TYPE_CHECKING:
    from app.models.produto import Produto
    from app.models.veiculo import VarianteVeiculo


class CompatibilidadeProdutoVeiculo(Base):
    __tablename__ = "compatibilidade_produtos_veiculos"
    __table_args__ = (
        UniqueConstraint(
            "produto_id", "variante_veiculo_id", name="compatibilidade_produto_variante_unique"
        ),
    )

    id: Mapped[UUIDType] = id_coluna()
    produto_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    variante_veiculo_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("variantes_veiculos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTimeType] = criado_em_coluna()

    produto: Mapped["Produto"] = relationship(back_populates="compatibilidades")
    variante: Mapped["VarianteVeiculo"] = relationship(back_populates="compatibilidades")
