from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_suggest():
    response = client.post(
        "/suggest",
        json={"query": "contraseña"}
    )
    assert response.status_code == 200
    assert "configuración" in response.json()["suggestion"]


def test_history():
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)