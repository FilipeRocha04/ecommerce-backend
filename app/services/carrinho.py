import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import DadosInvalidos, RecursoNaoEncontrado
from app.models.carrinho import Carrinho, ItemCarrinho
from app.models.enums import Canal
from app.repositories.carrinho import CarrinhoRepository
from app.repositories.estoque import EstoqueRepository
from app.repositories.produto import ProdutoRepository


class CarrinhoService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CarrinhoRepository(db)
        self.produto_repository = ProdutoRepository(db)
        self.estoque_repository = EstoqueRepository(db)

    def criar(
        self, *, usuario_id: uuid.UUID | None, sessao_id: str | None, canal: Canal
    ) -> Carrinho:
        carrinho = Carrinho(usuario_id=usuario_id, sessao_id=sessao_id, canal=canal)
        carrinho = self.repository.criar(carrinho)
        self.db.commit()
        self.db.refresh(carrinho)
        return carrinho

    def obter_por_id(self, carrinho_id: uuid.UUID) -> Carrinho:
        carrinho = self.repository.obter_por_id(carrinho_id)
        if carrinho is None:
            raise RecursoNaoEncontrado("Carrinho não encontrado.", codigo="carrinho_nao_encontrado")
        return carrinho

    def adicionar_item(
        self, carrinho_id: uuid.UUID, produto_id: uuid.UUID, quantidade: int
    ) -> Carrinho:
        if quantidade <= 0:
            raise DadosInvalidos(
                "Quantidade deve ser maior que zero.", codigo="quantidade_invalida"
            )

        self.obter_por_id(carrinho_id)

        produto = self.produto_repository.obter_por_id(produto_id)
        if produto is None:
            raise RecursoNaoEncontrado("Produto não encontrado.", codigo="produto_nao_encontrado")
        if not produto.ativo:
            raise DadosInvalidos(
                "Produto não está disponível para venda.", codigo="produto_inativo"
            )

        estoque = self.estoque_repository.obter_por_produto(produto_id)
        item_existente = self.repository.obter_item_por_produto(carrinho_id, produto_id)
        quantidade_total = quantidade + (item_existente.quantidade if item_existente else 0)

        disponivel = estoque.quantidade_disponivel if estoque else 0
        if quantidade_total > disponivel:
            raise DadosInvalidos(
                "Quantidade solicitada indisponível em estoque.", codigo="estoque_insuficiente"
            )

        preco_atual = produto.preco_promocional or produto.preco

        if item_existente:
            item_existente.quantidade = quantidade_total
            item_existente.preco_unitario = preco_atual
        else:
            item = ItemCarrinho(
                carrinho_id=carrinho_id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=preco_atual,
            )
            self.repository.adicionar_item(item)

        self.db.commit()
        return self.obter_por_id(carrinho_id)

    def atualizar_item(
        self, carrinho_id: uuid.UUID, item_id: uuid.UUID, quantidade: int
    ) -> Carrinho:
        if quantidade <= 0:
            raise DadosInvalidos(
                "Quantidade deve ser maior que zero.", codigo="quantidade_invalida"
            )

        self.obter_por_id(carrinho_id)
        item = self.repository.obter_item(carrinho_id, item_id)
        if item is None:
            raise RecursoNaoEncontrado(
                "Item não encontrado no carrinho.", codigo="item_carrinho_nao_encontrado"
            )

        estoque = self.estoque_repository.obter_por_produto(item.produto_id)
        disponivel = estoque.quantidade_disponivel if estoque else 0
        if quantidade > disponivel:
            raise DadosInvalidos(
                "Quantidade solicitada indisponível em estoque.", codigo="estoque_insuficiente"
            )

        item.quantidade = quantidade
        self.db.commit()
        return self.obter_por_id(carrinho_id)

    def remover_item(self, carrinho_id: uuid.UUID, item_id: uuid.UUID) -> Carrinho:
        self.obter_por_id(carrinho_id)
        item = self.repository.obter_item(carrinho_id, item_id)
        if item is None:
            raise RecursoNaoEncontrado(
                "Item não encontrado no carrinho.", codigo="item_carrinho_nao_encontrado"
            )
        self.repository.remover_item(item)
        self.db.commit()
        return self.obter_por_id(carrinho_id)
