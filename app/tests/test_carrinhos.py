import uuid

from fastapi.testclient import TestClient

from app.models.produto import Produto


def test_criar_carrinho(client: TestClient) -> None:
    resposta = client.post("/api/v1/carrinhos", json={"canal": "web"})
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["status"] == "ativo"
    assert corpo["itens"] == []


def test_adicionar_item_carrinho(client: TestClient, produto: Produto) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()

    resposta = client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 2},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["quantidade"] == 2


def test_adicionar_item_incrementa_quantidade_existente(
    client: TestClient, produto: Produto
) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()
    client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 2},
    )
    resposta = client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 1},
    )
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["quantidade"] == 3


def test_adicionar_item_quantidade_invalida(client: TestClient, produto: Produto) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()
    resposta = client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 0},
    )
    assert resposta.status_code == 422


def test_adicionar_item_estoque_insuficiente(client: TestClient, produto: Produto) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()
    resposta = client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 999},
    )
    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "estoque_insuficiente"


def test_atualizar_item_carrinho(client: TestClient, produto: Produto) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()
    item = client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 2},
    ).json()["itens"][0]

    resposta = client.patch(
        f"/api/v1/carrinhos/{carrinho['id']}/itens/{item['id']}", json={"quantidade": 5}
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"][0]["quantidade"] == 5


def test_remover_item_carrinho(client: TestClient, produto: Produto) -> None:
    carrinho = client.post("/api/v1/carrinhos", json={"canal": "web"}).json()
    item = client.post(
        f"/api/v1/carrinhos/{carrinho['id']}/itens",
        json={"produto_id": str(produto.id), "quantidade": 2},
    ).json()["itens"][0]

    resposta = client.delete(f"/api/v1/carrinhos/{carrinho['id']}/itens/{item['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_obter_carrinho_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/carrinhos/{uuid.uuid4()}")
    assert resposta.status_code == 404
