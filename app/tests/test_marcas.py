import uuid

from fastapi.testclient import TestClient

from app.models.marca import Marca


def test_listar_marcas(client: TestClient, marca: Marca) -> None:
    resposta = client.get("/api/v1/marcas")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["pagina"] == 1
    assert any(item["id"] == str(marca.id) for item in corpo["itens"])


def test_obter_marca(client: TestClient, marca: Marca) -> None:
    resposta = client.get(f"/api/v1/marcas/{marca.id}")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == marca.nome


def test_obter_marca_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/marcas/{uuid.uuid4()}")
    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "marca_nao_encontrada"
