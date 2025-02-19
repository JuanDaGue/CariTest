from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from api.schemas.history import HistoryResponse
from api.services.history_manager import get_history, reset_history

# Crear el router para manejar las rutas del historial
router = APIRouter()


def fetch_history(limit: int) -> List[HistoryResponse]:
    """
    Obtiene el historial de consultas y sugerencias almacenadas.

    - **limit**: Número máximo de registros a retornar.
    
    Retorna una lista con las consultas realizadas y sus respuestas.
    """
    return get_history(limit)


@router.get(
    "/",
    response_model=List[HistoryResponse],
    summary="Obtener historial de consultas",
    description="Devuelve el historial de consultas enviadas junto con sus respectivas sugerencias. Se puede limitar el número de resultados."
)
async def get_history_route(
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a obtener (1-100)"),
    history: List[HistoryResponse] = Depends(fetch_history)
):
    """
    Endpoint para obtener el historial de preguntas y respuestas.

    - **limit**: Límite de registros a devolver (entre 1 y 100).
    - **history**: Historial obtenido desde la función `fetch_history()`.
    """
    try:
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el historial: {str(e)}")


@router.post(
    "/reset",
    summary="Reiniciar historial",
    description="Limpia completamente el historial de consultas y respuestas almacenadas."
)
async def reset_history_route():
    """
    Endpoint para reiniciar el historial de consultas.

    - Elimina todas las consultas y respuestas almacenadas en la sesión actual.
    """
    try:
        reset_history()
        return {"success": True, "message": "Historial reiniciado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al reiniciar el historial: {str(e)}")
