from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuración global de la aplicación.
    """
    PROJECT_NAME: str = "Chat Assistant"
    HISTORY_MAX_SIZE: int = Field(default=1000, ge=1, description="Tamaño máximo del historial de consultas.")
    SIMILARITY_THRESHOLD: float = Field(default=0.4, ge=0.0, le=1.0, description="Umbral de similitud para coincidencias en FAQ.")
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY", description="Clave de API para Gemini.")
    FAQ_FILE: Path = Field(default=Path("data/dataChat.json"), description="Ruta al archivo de preguntas frecuentes.")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global de configuración
settings = Settings()
