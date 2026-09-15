import json
import uuid
from typing import Any

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.core.exceptions import ErroDominio
from app.models.enums import Canal
from app.models.produto import Produto
from app.services.carrinho import CarrinhoService
from app.services.compatibilidade import CompatibilidadeService
from app.services.estoque import EstoqueService
from app.services.produto import ProdutoService
from app.services.veiculo import VeiculoService


def _resumo_produto(produto: Produto) -> dict[str, Any]:
    preco = produto.preco_promocional or produto.preco
    return {
        "id": str(produto.id),
        "nome": produto.nome,
        "marca": produto.marca.nome,
        "sku": produto.sku,
        "preco": str(preco),
        "ativo": produto.ativo,
    }


def _resumo_carrinho(carrinho: Any) -> dict[str, Any]:
    return {
        "id": str(carrinho.id),
        "status": carrinho.status.value,
        "itens": [
            {
                "item_id": str(item.id),
                "produto_id": str(item.produto_id),
                "quantidade": item.quantidade,
                "preco_unitario": str(item.preco_unitario),
            }
            for item in carrinho.itens
        ],
    }


def criar_tools(db: Session, contexto: dict[str, Any]) -> list:
    """Cria as tools do agente, ligadas a uma sessão de banco e a um contexto
    mutável que acumula os produtos/carrinho tocados durante a conversa, para
    que a API possa devolver esses dados estruturados junto da resposta."""

    produto_service = ProdutoService(db)
    compatibilidade_service = CompatibilidadeService(db)
    estoque_service = EstoqueService(db)
    carrinho_service = CarrinhoService(db)
    veiculo_service = VeiculoService(db)

    def _registrar_produtos(produtos: list[Produto]) -> None:
        for produto in produtos:
            contexto["produtos"][produto.id] = produto

    @tool
    def buscar_variante_veiculo(
        fabricante: str = "", modelo: str = "", ano: int = 0, motor: str = ""
    ) -> str:
        """Resolve a descrição de um veículo (fabricante, modelo, ano e/ou motor)
        para o(s) variante_veiculo_id correspondente(s) no catálogo. Use esta
        ferramenta sempre que o cliente mencionar seu carro, antes de verificar
        compatibilidade ou buscar produtos filtrados por veículo — nunca invente
        um variante_veiculo_id."""
        variantes = veiculo_service.listar_variantes(
            fabricante=fabricante or None,
            modelo=modelo or None,
            ano=ano or None,
            motor=motor or None,
        )
        resumo = [
            {
                "variante_veiculo_id": str(v.id),
                "fabricante": v.fabricante_nome,
                "modelo": v.modelo_nome,
                "ano_inicio": v.ano_inicio,
                "ano_fim": v.ano_fim,
                "motor": v.motor,
                "combustivel": v.combustivel,
                "cambio": v.cambio,
            }
            for v in variantes
        ]
        return json.dumps(resumo, ensure_ascii=False)

    @tool
    def buscar_produtos(termo: str = "", variante_veiculo_id: str = "") -> str:
        """Busca peças no catálogo por termo de texto (nome, marca, código de peça).
        Se variante_veiculo_id for informado, retorna apenas peças compatíveis com
        essa variante de veículo. Use sempre esta ferramenta para encontrar
        produtos — nunca invente nome, preço ou existência de uma peça."""
        variante_id = uuid.UUID(variante_veiculo_id) if variante_veiculo_id else None
        if termo.strip():
            itens, _ = produto_service.buscar(termo.strip(), pagina=1, tamanho_pagina=10)
            if variante_id:
                itens = [p for p in itens if compatibilidade_service.verificar(p.id, variante_id)]
        else:
            itens, _ = produto_service.listar(
                pagina=1, tamanho_pagina=10, variante_veiculo_id=variante_id
            )
        _registrar_produtos(itens)
        return json.dumps([_resumo_produto(p) for p in itens], ensure_ascii=False)

    @tool
    def obter_produto(produto_id: str) -> str:
        """Obtém os detalhes completos de um produto específico pelo seu ID."""
        try:
            produto = produto_service.obter_por_id(uuid.UUID(produto_id))
        except ErroDominio as exc:
            return json.dumps({"erro": exc.mensagem})
        _registrar_produtos([produto])
        return json.dumps(_resumo_produto(produto), ensure_ascii=False)

    @tool
    def verificar_compatibilidade(produto_id: str, variante_veiculo_id: str) -> str:
        """Verifica se um produto específico é compatível com uma variante de
        veículo específica. Use antes de recomendar uma peça quando o cliente
        já informou o veículo."""
        try:
            compativel = compatibilidade_service.verificar(
                uuid.UUID(produto_id), uuid.UUID(variante_veiculo_id)
            )
        except ErroDominio as exc:
            return json.dumps({"erro": exc.mensagem})
        return json.dumps({"compativel": compativel})

    @tool
    def consultar_estoque(produto_id: str) -> str:
        """Consulta a quantidade disponível em estoque de um produto. Use antes
        de confirmar que uma peça está disponível para compra."""
        try:
            estoque = estoque_service.obter_por_produto(uuid.UUID(produto_id))
        except ErroDominio as exc:
            return json.dumps({"erro": exc.mensagem})
        return json.dumps({"quantidade_disponivel": estoque.quantidade_disponivel})

    @tool
    def obter_carrinho(carrinho_id: str) -> str:
        """Obtém o estado atual de um carrinho: itens, quantidades e preços."""
        try:
            carrinho = carrinho_service.obter_por_id(uuid.UUID(carrinho_id))
        except ErroDominio as exc:
            return json.dumps({"erro": exc.mensagem})
        contexto["carrinho_id"] = str(carrinho.id)
        return json.dumps(_resumo_carrinho(carrinho), ensure_ascii=False)

    @tool
    def adicionar_ao_carrinho(produto_id: str, quantidade: int, carrinho_id: str = "") -> str:
        """Adiciona uma quantidade de um produto ao carrinho de compras. Se
        carrinho_id estiver vazio, um novo carrinho é criado automaticamente.
        Só use depois que o cliente confirmar que quer a peça."""
        try:
            if carrinho_id:
                id_carrinho = uuid.UUID(carrinho_id)
            else:
                novo_carrinho = carrinho_service.criar(
                    usuario_id=None, sessao_id=None, canal=Canal.ASSISTENTE
                )
                id_carrinho = novo_carrinho.id
            carrinho = carrinho_service.adicionar_item(
                id_carrinho, uuid.UUID(produto_id), quantidade
            )
        except ErroDominio as exc:
            return json.dumps({"erro": exc.mensagem})
        contexto["carrinho_id"] = str(carrinho.id)
        return json.dumps(_resumo_carrinho(carrinho), ensure_ascii=False)

    @tool
    def remover_do_carrinho(carrinho_id: str, item_id: str) -> str:
        """Remove um item do carrinho de compras."""
        try:
            carrinho = carrinho_service.remover_item(uuid.UUID(carrinho_id), uuid.UUID(item_id))
        except ErroDominio as exc:
            return json.dumps({"erro": exc.mensagem})
        contexto["carrinho_id"] = str(carrinho.id)
        return json.dumps(_resumo_carrinho(carrinho), ensure_ascii=False)

    return [
        buscar_variante_veiculo,
        buscar_produtos,
        obter_produto,
        verificar_compatibilidade,
        consultar_estoque,
        obter_carrinho,
        adicionar_ao_carrinho,
        remover_do_carrinho,
    ]
