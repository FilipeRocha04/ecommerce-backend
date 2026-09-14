import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.pedido import ItemPedido, Pedido


class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.flush()
        return pedido

    def obter_por_id(self, pedido_id: uuid.UUID) -> Pedido | None:
        query = select(Pedido).where(Pedido.id == pedido_id).options(joinedload(Pedido.itens))
        return self.db.execute(query).unique().scalar_one_or_none()

    def listar_por_usuario(
        self, usuario_id: uuid.UUID, *, offset: int, limite: int
    ) -> tuple[list[Pedido], int]:
        query_base = select(Pedido).where(Pedido.usuario_id == usuario_id)
        total = self.db.query(Pedido).where(Pedido.usuario_id == usuario_id).count()
        query = (
            query_base.options(joinedload(Pedido.itens))
            .order_by(Pedido.created_at.desc())
            .offset(offset)
            .limit(limite)
        )
        itens = self.db.execute(query).unique().scalars().all()
        return list(itens), total

    def existe_numero_pedido(self, numero_pedido: str) -> bool:
        query = select(Pedido.id).where(Pedido.numero_pedido == numero_pedido)
        return self.db.scalar(query) is not None

    def adicionar_item(self, item: ItemPedido) -> ItemPedido:
        self.db.add(item)
        return item
