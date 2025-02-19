from pydantic import BaseModel, Field

class FAQRequest(BaseModel):
    """
    Modelo para la solicitud de sugerencias de preguntas frecuentes.

    - `query`: Pregunta ingresada por el usuario.
    """
    query: str = Field(..., min_length=1, description="La consulta no puede estar vacía")


class FAQResponse(BaseModel):
    """
    Modelo para la respuesta de preguntas frecuentes.

    - `query`: Pregunta original enviada por el usuario.
    - `suggestion`: Respuesta sugerida basada en la base de conocimiento.
    - `confidence`: Nivel de confianza de la sugerencia.
    """
    query: str
    suggestion: str
    confidence: float
