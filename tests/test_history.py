from fastapi.testclient import TestClient
from main import app
from api.services.history_manager import reset_history

client = TestClient(app)

def test_get_history():
    reset_history()
    response = client.get("/history/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_reset_history():
    response = client.post("/history/reset")
    assert response.status_code == 200
    assert response.json()["success"] is True