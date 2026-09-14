import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.compatibilidade import CompatibilidadeProdutoVeiculo
from app.models.produto import Produto
from app.models.veiculo import VarianteVeiculo


def test_compatibilidade_positiva(
    client: TestClient, db: Session, produto: Produto, variante: VarianteVeiculo
) -> None:
    db.add(CompatibilidadeProdutoVeiculo(produto_id=produto.id, variante_veiculo_id=variante.id))
    db.flush()

    resposta = client.get(
        "/api/v1/compatibilidade",
        params={"produto_id": str(produto.id), "variante_veiculo_id": str(variante.id)},
    )
    assert resposta.status_code == 200
    assert resposta.json()["compativel"] is True


def test_compatibilidade_negativa(
    client: TestClient, produto: Produto, variante: VarianteVeiculo
) -> None:
    resposta = client.get(
        "/api/v1/compatibilidade",
        params={"produto_id": str(produto.id), "variante_veiculo_id": str(variante.id)},
    )
    assert resposta.status_code == 200
    assert resposta.json()["compativel"] is False


def test_compatibilidade_produto_inexistente(client: TestClient, variante: VarianteVeiculo) -> None:
    resposta = client.get(
        "/api/v1/compatibilidade",
        params={"produto_id": str(uuid.uuid4()), "variante_veiculo_id": str(variante.id)},
    )
    assert resposta.status_code == 404
