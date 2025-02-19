from typing import Dict, Union
import json
from difflib import get_close_matches
from config.config import settings

# Cargar base de conocimiento desde el archivo JSON
try:
    with open(settings.FAQ_FILE, "r", encoding="utf-8") as f:
        faqs = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: No se encontró el archivo {settings.FAQ_FILE}. Verifica la configuración.")

# Lista de saludos comunes en diferentes idiomas
SALUDOS = {
    "hola", "buenos días", "buenas tardes", "buenas noches",
    "hi", "hello", "saludos", "qué tal", "cómo estás"
}


def es_saludo(query: str) -> bool:
    """
    Determina si la consulta es un saludo.

    Args:
        query (str): Texto de entrada del usuario.

    Returns:
        bool: True si el texto es un saludo, False en caso contrario.
    """
    return query.lower().strip() in SALUDOS


def get_suggestion(query: str) -> Dict[str, Union[str, float]]:
    """
    Obtiene una respuesta sugerida basada en la pregunta del usuario.

    Args:
        query (str): Pregunta del usuario.

    Returns:
        Dict[str, Union[str, float]]: Diccionario con la respuesta, nivel de confianza y pregunta coincidente.
    """

    # Manejar saludos de forma directa
    if es_saludo(query):
        return {
            "response": "¡Hola! Soy un asistente virtual. ¿En qué puedo ayudarte hoy?",
            "confidence": 1.0,
            "matched_question": "Saludo"
        }

    # Obtener lista de preguntas de la base de conocimiento
    questions = [faq["pregunta"] for faq in faqs]

    # Buscar coincidencias con la pregunta del usuario
    matches = get_close_matches(
        query.lower(),
        [q.lower() for q in questions],
        n=1,
        cutoff=settings.SIMILARITY_THRESHOLD  # Umbral de similitud definido en la configuración
    )

    # Si hay una coincidencia, obtener la pregunta y respuesta asociadas
    if matches:
        original_question = next(q for q in questions if q.lower() == matches[0])
        answer = next(faq["respuesta"] for faq in faqs if faq["pregunta"] == original_question)

        return {
            "response": answer,
            "confidence": round(len(matches[0]) / len(query), 2),  # Confianza basada en la longitud de la coincidencia
            "matched_question": original_question
        }

    # Si no hay coincidencias, devolver una respuesta predeterminada
    return {
        "response": "No encontré una respuesta específica. ¿Podrías proporcionar más detalles?",
        "confidence": 0.0,
        "matched_question": ""
    }
