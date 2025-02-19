from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """
    Modelo para la solicitud de chat.

    - `prompt`: Entrada del usuario.
    - `context`: Contexto opcional para mejorar la respuesta del chatbot.
    """
    prompt: str
    context: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Modelo para la respuesta del chat.

    - `success`: Indica si la operación fue exitosa.
    - `prompt`: Entrada original del usuario.
    - `response`: Respuesta generada por la IA.
    - `error`: Mensaje de error opcional en caso de fallo.
    """
    success: bool
    prompt: str
    response: str
    error: Optional[str] = None
