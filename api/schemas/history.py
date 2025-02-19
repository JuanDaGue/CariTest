from datetime import datetime
from pydantic import BaseModel, Field

class HistoryResponse(BaseModel):
    """
    Modelo de respuesta para el historial de consultas.

    Atributos:
    - `timestamp` (datetime): Momento en que se realizó la consulta.
    - `query` (str): Pregunta ingresada por el usuario.
    - `suggestion` (str): Respuesta sugerida basada en la base de conocimiento.
    - `confidence` (float): Nivel de confianza de la sugerencia.
    - `matched_question` (str): Pregunta de la base de conocimiento que mejor coincide.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de la consulta")
    query: str = Field(..., min_length=1, description="Pregunta ingresada por el usuario")
    suggestion: str = Field(..., description="Sugerencia basada en la base de conocimiento")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza en la coincidencia (0-1)")
    matched_question: str = Field(..., description="Pregunta coincidente en la base de conocimiento")
