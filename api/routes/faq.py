from fastapi import APIRouter, HTTPException, Depends
from api.schemas.faq import FAQRequest, FAQResponse
from api.services.faq_suggest import get_suggestion
from api.services.history_manager import add_to_history

# Crear el router para manejar solicitudes de FAQ
router = APIRouter()


# Dependencia para obtener la sugerencia basada en la consulta del usuario
def fetch_suggestion(query: str):
    """
    Obtiene una sugerencia basada en la consulta ingresada por el usuario.
    Retorna un diccionario con:
    - "response": Respuesta sugerida.
    - "confidence": Nivel de confianza de la sugerencia.
    """
    return get_suggestion(query)


@router.post(
    "/suggest",
    response_model=FAQResponse,
    summary="Obtiene una sugerencia basada en preguntas frecuentes",
)
async def suggest_faq(query: FAQRequest):
    """
    Retorna una sugerencia automática basada en preguntas frecuentes.

    - **query**: Consulta del usuario.

    La sugerencia se obtiene de la base de conocimiento y se almacena en el historial.
    """
    try:
        # Validar que la consulta no esté vacía
        user_query = query.query.strip()
        if not user_query:
            raise HTTPException(
                status_code=400, detail="La consulta no puede estar vacía"
            )

        # Obtener la sugerencia
        suggestion = fetch_suggestion(user_query)

        # Agregar la consulta y la sugerencia al historial
        add_to_history(user_query, suggestion)

        # Retornar la respuesta formateada
        return FAQResponse(
            query=user_query,
            suggestion=suggestion["response"],
            confidence=suggestion["confidence"],
        )

    except HTTPException as http_err:
        raise http_err  # Re-lanzar errores HTTP controlados

    except Exception as e:
        error_message = f"Error interno al procesar la solicitud: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
