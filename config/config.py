# config/config.py
from pydantic_settings import BaseSettings  # Cambia esta línea
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat Assistant"
    HISTORY_MAX_SIZE: int = 1000
    SIMILARITY_THRESHOLD: float = 0.4
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    FAQ_FILE: str = "data/dataChat.json"

    class Config:
        env_file = ".env"


settings = Settings()
