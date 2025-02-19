from fastapi.testclient import TestClient
from main import app
from api.services.history_manager import reset_history, add_to_history

client = TestClient(app)


def test_get_history():
    reset_history()
    response = client.get("/history/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0  # Validar que está vacío después del reset


def test_add_and_get_history():
    reset_history()
    
    test_query = "¿Cómo cambio mi contraseña?"
    test_suggestion = {
        "response": "Puedes cambiar tu contraseña en la configuración de tu perfil.",
        "confidence": 0.9,
        "matched_question": "¿Cómo cambio mi contraseña?"
    }
    
    add_to_history(test_query, test_suggestion)
    
    response = client.get("/history/")
    assert response.status_code == 200
    history_data = response.json()
    
    assert isinstance(history_data, list)
    assert len(history_data) == 1  # Asegurar que el historial contiene un elemento
    assert history_data[0]["query"] == test_query
    assert history_data[0]["suggestion"] == test_suggestion["response"]


def test_reset_history():
    response = client.post("/history/reset")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Asegurar que el historial está vacío después del reset
    response = client.get("/history/")
    assert response.status_code == 200
    assert len(response.json()) == 0
