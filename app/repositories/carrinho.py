import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.carrinho import Carrinho, ItemCarrinho


class CarrinhoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, carrinho: Carrinho) -> Carrinho:
        self.db.add(carrinho)
        self.db.flush()
        return carrinho

    def obter_por_id(self, carrinho_id: uuid.UUID) -> Carrinho | None:
        query = (
            select(Carrinho).where(Carrinho.id == carrinho_id).options(joinedload(Carrinho.itens))
        )
        return self.db.execute(query).unique().scalar_one_or_none()

    def obter_item(self, carrinho_id: uuid.UUID, item_id: uuid.UUID) -> ItemCarrinho | None:
        query = select(ItemCarrinho).where(
            ItemCarrinho.id == item_id, ItemCarrinho.carrinho_id == carrinho_id
        )
        return self.db.execute(query).scalar_one_or_none()

    def obter_item_por_produto(
        self, carrinho_id: uuid.UUID, produto_id: uuid.UUID
    ) -> ItemCarrinho | None:
        query = select(ItemCarrinho).where(
            ItemCarrinho.carrinho_id == carrinho_id, ItemCarrinho.produto_id == produto_id
        )
        return self.db.execute(query).scalar_one_or_none()

    def adicionar_item(self, item: ItemCarrinho) -> ItemCarrinho:
        self.db.add(item)
        self.db.flush()
        return item

    def remover_item(self, item: ItemCarrinho) -> None:
        self.db.delete(item)
        self.db.flush()
