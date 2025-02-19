from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    """
    Modelo base para respuestas API.

    - `success`: Indica si la operación fue exitosa (por defecto `True`).
    - `error`: Mensaje de error opcional en caso de fallo.
    """
    success: bool = True
    error: Optional[str] = None
