import uuid

from fastapi.testclient import TestClient

from app.models.produto import Produto


def test_listar_produtos(client: TestClient, produto: Produto) -> None:
    resposta = client.get("/api/v1/produtos")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert any(item["id"] == str(produto.id) for item in corpo["itens"])


def test_obter_produto(client: TestClient, produto: Produto) -> None:
    resposta = client.get(f"/api/v1/produtos/{produto.id}")
    assert resposta.status_code == 200
    assert resposta.json()["sku"] == produto.sku


def test_obter_produto_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/produtos/{uuid.uuid4()}")
    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "produto_nao_encontrado"


def test_buscar_produtos(client: TestClient, produto: Produto) -> None:
    resposta = client.get("/api/v1/produtos/buscar", params={"q": "Pastilha"})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert any(item["id"] == str(produto.id) for item in corpo["itens"])


def test_buscar_produtos_parametro_obrigatorio(client: TestClient) -> None:
    resposta = client.get("/api/v1/produtos/buscar")
    assert resposta.status_code == 422


def test_obter_estoque_produto(client: TestClient, produto: Produto) -> None:
    resposta = client.get(f"/api/v1/produtos/{produto.id}/estoque")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["quantidade"] == 10
    assert corpo["quantidade_reservada"] == 2
    assert corpo["quantidade_disponivel"] == 8


def test_obter_estoque_produto_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/produtos/{uuid.uuid4()}/estoque")
    assert resposta.status_code == 404
