from fastapi.testclient import TestClient


def test_conversar_sem_openai_configurado(client: TestClient) -> None:
    resposta = client.post("/api/v1/assistente/conversar", json={"mensagem": "Olá"})
    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "assistente_nao_configurado"
