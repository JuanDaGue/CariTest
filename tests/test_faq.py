from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_suggest_faq():
    response = client.post(
        "/faq/suggest",
        json={"query": "¿Cómo cambio mi contraseña?"}
    )
    assert response.status_code == 200
    assert "configuración" in response.json()["suggestion"]