from fastapi.testclient import TestClient
from main import app
from api.schemas.chat import ChatResponse
import pytest

client = TestClient(app)

# Mock de la respuesta de Gemini
MOCK_GEMINI_RESPONSE = "¡Hola! Soy Gemini, tu asistente de IA."

def test_chat_generate_success(monkeypatch):
    # Mock de la función generate_response de GeminiClient
    def mock_generate_response(*args, **kwargs):
        return MOCK_GEMINI_RESPONSE

    # Aplicar el mock
    monkeypatch.setattr(
        "api.services.gemini.GeminiClient.generate_response",
        mock_generate_response
    )

    # Datos de prueba
    test_data = {
        "prompt": "Hola, ¿cómo estás?",
        "context": "Saludo informal"
    }

    # Llamar al endpoint
    response = client.post("/chat/generate", json=test_data)

    # Verificaciones
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "prompt": test_data["prompt"],
        "response": MOCK_GEMINI_RESPONSE,
        "error": None
    }

def test_chat_generate_empty_prompt():
    # Datos de prueba con prompt vacío
    test_data = {
        "prompt": "",
        "context": "Saludo informal"
    }

    # Llamar al endpoint
    response = client.post("/chat/generate", json=test_data)

    # Verificaciones
    assert response.status_code == 400
    assert "El prompt no puede estar vacío" in response.json()["detail"]

def test_chat_generate_gemini_error(monkeypatch):
    # Mock para simular un error en Gemini
    def mock_generate_response(*args, **kwargs):
        raise Exception("Error en la API de Gemini")

    # Aplicar el mock
    monkeypatch.setattr(
        "api.services.gemini.GeminiClient.generate_response",
        mock_generate_response
    )

    # Datos de prueba
    test_data = {
        "prompt": "Hola, ¿cómo estás?",
        "context": "Saludo informal"
    }

    # Llamar al endpoint
    response = client.post("/chat/generate", json=test_data)

    # Verificaciones
    assert response.status_code == 500
    assert "Error interno" in response.json()["detail"]
