import uuid

from fastapi.testclient import TestClient

from app.models.categoria import Categoria


def test_listar_categorias(client: TestClient, categoria: Categoria) -> None:
    resposta = client.get("/api/v1/categorias")
    assert resposta.status_code == 200
    assert any(item["id"] == str(categoria.id) for item in resposta.json())


def test_obter_categoria(client: TestClient, categoria: Categoria) -> None:
    resposta = client.get(f"/api/v1/categorias/{categoria.id}")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == categoria.nome


def test_obter_categoria_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/categorias/{uuid.uuid4()}")
    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "categoria_nao_encontrada"
