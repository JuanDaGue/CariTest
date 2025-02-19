from difflib import get_close_matches
import json
from typing import Dict
from config.config import settings

# Cargar base de conocimiento
with open(settings.FAQ_FILE, "r") as f:
    faqs = json.load(f)

questions = [faq["pregunta"] for faq in faqs]

def get_suggestion(query: str) -> Dict:
    # Preprocesar la consulta
    processed_query = query.lower().strip()

    # Búsqueda exacta
    exact_match = next(
        (faq for faq in faqs if faq["pregunta"].lower() == processed_query),
        None
    )
    if exact_match:
        return {
            "response": exact_match["respuesta"],
            "confidence": 1.0,
            "matched_question": exact_match["pregunta"]
        }

    # Búsqueda aproximada
    matches = get_close_matches(
        processed_query,
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
            "confidence": round(len(matches[0])/len(processed_query), 2),
            "matched_question": original_question
        }

    return {
        "response": "Por favor contacte al soporte técnico para ayuda adicional.",
        "confidence": 0.0,
        "matched_question": ""
    }
