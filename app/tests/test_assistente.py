import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.services import assistente as assistente_module


def test_conversar_sem_openai_configurado(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(assistente_module, "get_settings", lambda: Settings(openai_api_key=""))

    resposta = client.post("/api/v1/assistente/conversar", json={"mensagem": "Olá"})
    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "assistente_nao_configurado"
