from collections import deque
from datetime import datetime
from typing import List, Dict
from config.config import settings

# Estructura de datos para el historial
history: deque = deque(maxlen=settings.HISTORY_MAX_SIZE)


def add_to_history(query: str, suggestion: Dict):
    history.append({
        "timestamp": datetime.now(),
        "query": query,
        "suggestion": suggestion["response"],
        "confidence": suggestion["confidence"],
        "matched_question": suggestion["matched_question"]
    })


def get_history(limit: int = 10) -> List[Dict]:
    return list(history)[-limit:]


def reset_history():
    global history
    history = deque(maxlen=settings.HISTORY_MAX_SIZE)