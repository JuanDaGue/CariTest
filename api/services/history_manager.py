from collections import deque
from datetime import datetime
from typing import List, Dict, Any
from config.config import settings

# Inicializar historial con un tamaño máximo configurable
history: deque[Dict[str, Any]] = deque(maxlen=settings.HISTORY_MAX_SIZE)


def add_to_history(query: str, suggestion: Dict[str, Any]) -> None:
    """
    Agrega una consulta y su respuesta al historial.

    Args:
        query (str): La consulta realizada por el usuario.
        suggestion (Dict[str, Any]): Respuesta generada y detalles adicionales.

    Raises:
        ValueError: Si `suggestion` no contiene los campos esperados.
    """
    required_keys = {"response", "confidence", "matched_question"}
    if not required_keys.issubset(suggestion.keys()):
        raise ValueError("El diccionario 'suggestion' debe contener 'response', 'confidence' y 'matched_question'.")

    history.append({
        "timestamp": datetime.now(),
        "query": query.strip(),
        "suggestion": suggestion["response"],
        "confidence": round(suggestion["confidence"], 2),
        "matched_question": suggestion["matched_question"]
    })


def get_history(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retorna los últimos elementos del historial.

    Args:
        limit (int, opcional): Cantidad máxima de registros a devolver. Por defecto, 10.

    Returns:
        List[Dict[str, Any]]: Lista con los últimos elementos del historial.
    """
    return list(history)[-limit:]


def reset_history() -> None:
    """
    Reinicia el historial de consultas.
    """
    history.clear()
