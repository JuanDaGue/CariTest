from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Mock de la respuesta de fetch_suggestion
MOCK_SUGGESTION_RESPONSE = {
    "query": "¿Cómo cambio mi contraseña?",
    "suggestion": "Puedes cambiar tu contraseña en la sección de configuración de tu perfil.",
    "confidence": 1,
}


def test_suggest_faq_success(monkeypatch):
    # Mock de la función fetch_suggestion
    def mock_fetch_suggestion(*args, **kwargs):
        return MOCK_SUGGESTION_RESPONSE

    # Datos de prueba
    test_data = {"query": "¿Cómo cambio mi contraseña?"}

    # Llamar al endpoint
    response = client.post("/faq/suggest", json=test_data)

    # Verificaciones
    assert response.status_code == 200
    assert response.json() == {
        "query": test_data["query"],
        "suggestion": MOCK_SUGGESTION_RESPONSE["suggestion"],
        "confidence": MOCK_SUGGESTION_RESPONSE["confidence"],
    }


def test_suggest_faq_internal_error(monkeypatch):
    # Mock para simular un error interno en fetch_suggestion
    def mock_fetch_suggestion(*args, **kwargs):
        raise Exception("Error interno en fetch_suggestion")

    # Aplicar el mock
    monkeypatch.setattr("api.routes.faq.fetch_suggestion", mock_fetch_suggestion)

    # Datos de prueba
    test_data = {"query": "¿Cómo cambio mi contraseña?"}

    # Llamar al endpoint
    response = client.post("/faq/suggest", json=test_data)

    # Verificaciones
    assert response.status_code == 500
    assert "Error interno al procesar la solicitud" in response.json()["detail"]
