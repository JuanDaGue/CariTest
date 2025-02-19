from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_suggest_faq():
    response = client.post(
        "/faq/suggest",
        json={"query": "¿Cómo puedo modificar mi clave?"}  # Variación de la pregunta
    )
    assert response.status_code == 200
    data = response.json()

    # Verificar estructura de la respuesta
    assert "suggestion" in data
    assert "confidence" in data
    assert "matched_question" in data

    # Verificar contenido de la sugerencia
    assert "configuración" in data["suggestion"]
    assert data["confidence"] >= 0.4  # Si usas un umbral de similitud
