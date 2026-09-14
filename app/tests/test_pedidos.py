import uuid

from fastapi.testclient import TestClient

from app.models.produto import Produto
from app.models.usuario import Usuario


def _criar_carrinho_com_item(client: TestClient, produto: Produto, quantidade: int = 2) -> str:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()
    client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": quantidade},
    )
    return carrinho["id"]


def test_criar_pedido(client: TestClient, produto: Produto, usuario: Usuario) -> None:
    carrinho_id = _criar_carrinho_com_item(client, produto)

    resposta = client.post(
        "/api/v1/pedidos",
        json={
            "usuario_id": str(usuario.id),
            "carrinho_id": carrinho_id,
            "endereco_entrega": {
                "cep": "01310-100",
                "logradouro": "Av. Paulista",
                "numero": "1000",
                "bairro": "Bela Vista",
                "cidade": "São Paulo",
                "estado": "SP",
            },
        },
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["status"] == "aguardando_pagamento"
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["quantidade"] == 2


def test_criar_pedido_carrinho_vazio(client: TestClient, usuario: Usuario) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()

    resposta = client.post(
        "/api/v1/pedidos",
        json={
            "usuario_id": str(usuario.id),
            "carrinho_id": carrinho["id"],
            "endereco_entrega": {"cidade": "São Paulo"},
        },
    )
    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "carrinho_vazio"


def test_obter_pedido(client: TestClient, produto: Produto, usuario: Usuario) -> None:
    carrinho_id = _criar_carrinho_com_item(client, produto)
    pedido = client.post(
        "/api/v1/pedidos",
        json={
            "usuario_id": str(usuario.id),
            "carrinho_id": carrinho_id,
            "endereco_entrega": {"cidade": "São Paulo"},
        },
    ).json()

    resposta = client.get(f"/api/v1/pedidos/{pedido['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["numero_pedido"] == pedido["numero_pedido"]


def test_obter_pedido_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/pedidos/{uuid.uuid4()}")
    assert resposta.status_code == 404


def test_listar_pedidos_por_usuario(client: TestClient, produto: Produto, usuario: Usuario) -> None:
    carrinho_id = _criar_carrinho_com_item(client, produto)
    client.post(
        "/api/v1/pedidos",
        json={
            "usuario_id": str(usuario.id),
            "carrinho_id": carrinho_id,
            "endereco_entrega": {"cidade": "São Paulo"},
        },
    )

    resposta = client.get("/api/v1/pedidos", params={"usuario_id": str(usuario.id)})
    assert resposta.status_code == 200
    assert resposta.json()["total"] == 1
