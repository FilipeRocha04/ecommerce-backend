import uuid

from fastapi.testclient import TestClient

from app.models.veiculo import FabricanteVeiculo, ModeloVeiculo, VarianteVeiculo


def test_listar_fabricantes(client: TestClient, fabricante: FabricanteVeiculo) -> None:
    resposta = client.get("/api/v1/veiculos/fabricantes")
    assert resposta.status_code == 200
    assert any(item["id"] == str(fabricante.id) for item in resposta.json())


def test_obter_fabricante_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/veiculos/fabricantes/{uuid.uuid4()}")
    assert resposta.status_code == 404


def test_listar_modelos(client: TestClient, modelo: ModeloVeiculo) -> None:
    resposta = client.get("/api/v1/veiculos/modelos")
    assert resposta.status_code == 200
    assert any(item["id"] == str(modelo.id) for item in resposta.json())


def test_obter_modelo_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/veiculos/modelos/{uuid.uuid4()}")
    assert resposta.status_code == 404


def test_listar_variantes(client: TestClient, variante: VarianteVeiculo) -> None:
    resposta = client.get("/api/v1/veiculos/variantes", params={"ano": 2020})
    assert resposta.status_code == 200
    assert any(item["id"] == str(variante.id) for item in resposta.json())


def test_obter_variante_inexistente(client: TestClient) -> None:
    resposta = client.get(f"/api/v1/veiculos/variantes/{uuid.uuid4()}")
    assert resposta.status_code == 404
