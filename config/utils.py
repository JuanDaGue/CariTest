from functools import lru_cache


@lru_cache(maxsize=128)
def preprocess_text(text: str) -> str:
    text = text.lower().strip()
    return "".join(c for c in text if c.isalnum() or c.isspace())
