from typing import Dict, Union
import json
from difflib import get_close_matches
from config.config import settings

# Cargar base de conocimiento
with open(settings.FAQ_FILE, "r") as f:
    faqs = json.load(f)

# Lista de saludos comunes
SALUDOS = [
    "hola", "buenos días", "buenas tardes", "buenas noches",
    "hi", "hello", "saludos", "qué tal", "cómo estás"
]


def es_saludo(query: str) -> bool:
    """Determina si la consulta es un saludo."""
    query = query.lower().strip()
    return any(saludo in query for saludo in SALUDOS)


def get_suggestion(query: str) -> Dict[str, Union[str, float]]:
    # Manejar saludos
    if es_saludo(query):
        return {
            "response": "¡Hola! Soy un asistente virtual. ¿En qué puedo ayudarte hoy?",
            "confidence": 1.0,
            "matched_question": "Saludo"
        }

    # Búsqueda en FAQs
    questions = [faq["pregunta"] for faq in faqs]
    matches = get_close_matches(
        query.lower(),
        [q.lower() for q in questions],
        n=1,
        cutoff=settings.SIMILARITY_THRESHOLD
    )

    if matches:
        original_question = next(
            q for q in questions if q.lower() == matches[0]
        )
        answer = next(
            faq["respuesta"] for faq in faqs if faq["pregunta"] == original_question
        )
        return {
            "response": answer,
            "confidence": round(len(matches[0])/len(query), 2),
            "matched_question": original_question
        }

    return {
        "response": "No encontré una respuesta específica. ¿Podrías proporcionar más detalles?",
        "confidence": 0.0,
        "matched_question": ""
    }
