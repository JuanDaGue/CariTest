from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

# Mock de la respuesta del historial
MOCK_HISTORY_RESPONSE = [
    {
        "query": "¿Cómo cambio mi contraseña?",
        "suggestion": "Puedes cambiar tu contraseña en la sección de configuración de tu perfil.",
        "timestamp": "2025-02-17T00:59:32",
        "confidence": 1.0,
        "matched_question": "¿Cómo cambio mi contraseña?",
    }
]

# Mock de la respuesta al reiniciar el historial
MOCK_RESET_RESPONSE = {"success": True, "message": "Historial reiniciado con éxito"}


@patch("api.services.history_manager.get_history", return_value=MOCK_HISTORY_RESPONSE)
def test_get_history_success(mock_get_history):
    response = client.get("/history?limit=10")
    assert response.status_code == 200
    response_data = response.json()
    expected_data = MOCK_HISTORY_RESPONSE
    assert response_data[0]["query"] == expected_data[0]["query"]
    assert response_data[0]["suggestion"] == expected_data[0]["suggestion"]
    assert response_data[0]["confidence"] == expected_data[0]["confidence"]
    assert response_data[0]["matched_question"] == expected_data[0]["matched_question"]


@patch("api.services.history_manager.reset_history", return_value=None)
def test_reset_history_success(mock_reset_history):
    response = client.post("/history/reset")
    assert response.status_code == 200
    assert response.json() == MOCK_RESET_RESPONSE
