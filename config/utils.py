from functools import lru_cache
import re

@lru_cache(maxsize=128)
def preprocess_text(text: str) -> str:
    """
    Normaliza el texto convirtiéndolo a minúsculas, eliminando espacios extra 
    y eliminando caracteres especiales, manteniendo solo letras, números y espacios.
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)  # Mantiene solo letras, números y espacios
    text = re.sub(r"\s+", " ", text)  # Reemplaza múltiples espacios por uno solo
    return text
