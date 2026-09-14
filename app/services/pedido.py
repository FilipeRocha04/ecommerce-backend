import random
import string
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import DadosInvalidos, RecursoNaoEncontrado
from app.models.enums import StatusCarrinho, StatusPedido
from app.models.pedido import ItemPedido, Pedido
from app.repositories.carrinho import CarrinhoRepository
from app.repositories.estoque import EstoqueRepository
from app.repositories.pedido import PedidoRepository


def _gerar_numero_pedido() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    sufixo = "".join(random.choices(string.digits, k=4))
    return f"PED-{timestamp}-{sufixo}"


class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PedidoRepository(db)
        self.carrinho_repository = CarrinhoRepository(db)
        self.estoque_repository = EstoqueRepository(db)

    def criar(
        self, *, usuario_id: uuid.UUID, carrinho_id: uuid.UUID, endereco_entrega: dict[str, Any]
    ) -> Pedido:
        carrinho = self.carrinho_repository.obter_por_id(carrinho_id)
        if carrinho is None:
            raise RecursoNaoEncontrado("Carrinho não encontrado.", codigo="carrinho_nao_encontrado")
        if not carrinho.itens:
            raise DadosInvalidos("Carrinho está vazio.", codigo="carrinho_vazio")
        if carrinho.status != StatusCarrinho.ATIVO:
            raise DadosInvalidos("Carrinho não está ativo.", codigo="carrinho_nao_ativo")

        for item in carrinho.itens:
            estoque = self.estoque_repository.obter_por_produto(item.produto_id)
            disponivel = estoque.quantidade_disponivel if estoque else 0
            if item.quantidade > disponivel:
                raise DadosInvalidos(
                    "Quantidade solicitada indisponível em estoque.",
                    codigo="estoque_insuficiente",
                )

        subtotal = sum(item.preco_unitario * item.quantidade for item in carrinho.itens)
        desconto = 0
        frete = 0
        total = subtotal - desconto + frete

        numero_pedido = _gerar_numero_pedido()
        while self.repository.existe_numero_pedido(numero_pedido):
            numero_pedido = _gerar_numero_pedido()

        pedido = Pedido(
            numero_pedido=numero_pedido,
            usuario_id=usuario_id,
            status=StatusPedido.AGUARDANDO_PAGAMENTO,
            subtotal=subtotal,
            desconto=desconto,
            frete=frete,
            total=total,
            canal=carrinho.canal,
            endereco_entrega=endereco_entrega,
        )
        self.repository.criar(pedido)

        for item in carrinho.itens:
            self.repository.adicionar_item(
                ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=item.produto_id,
                    sku=item.produto.sku,
                    nome_produto=item.produto.nome,
                    quantidade=item.quantidade,
                    preco_unitario=item.preco_unitario,
                    total=item.preco_unitario * item.quantidade,
                )
            )
            estoque = self.estoque_repository.obter_por_produto(item.produto_id)
            if estoque is not None:
                estoque.quantidade_reservada += item.quantidade

        carrinho.status = StatusCarrinho.CONVERTIDO

        self.db.commit()
        return self.obter_por_id(pedido.id)

    def obter_por_id(self, pedido_id: uuid.UUID) -> Pedido:
        pedido = self.repository.obter_por_id(pedido_id)
        if pedido is None:
            raise RecursoNaoEncontrado("Pedido não encontrado.", codigo="pedido_nao_encontrado")
        return pedido

    def listar_por_usuario(
        self, usuario_id: uuid.UUID, *, pagina: int, tamanho_pagina: int
    ) -> tuple[list[Pedido], int]:
        offset = (pagina - 1) * tamanho_pagina
        return self.repository.listar_por_usuario(usuario_id, offset=offset, limite=tamanho_pagina)
