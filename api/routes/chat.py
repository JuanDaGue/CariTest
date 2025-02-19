from fastapi import APIRouter, HTTPException, Depends
from api.schemas.chat import ChatRequest, ChatResponse
from api.services.gemini import GeminiClient
from typing import Annotated

# Crear el router de la API para manejar las solicitudes de chat
router = APIRouter()

# Función para obtener la instancia de GeminiClient (inyección de dependencias)


def get_gemini_client() -> GeminiClient:
    return GeminiClient()


@router.post("/generate", response_model=ChatResponse, summary="Genera una respuesta usando Gemini")
async def chat_with_gemini(
    request: ChatRequest,
    gemini_client: Annotated[GeminiClient, Depends(get_gemini_client)]
):
    """
    Genera una respuesta basada en el prompt proporcionado utilizando Gemini.

    - **prompt**: Texto con la consulta del usuario.
    - **context**: Contexto opcional para mejorar la respuesta.
    
    Retorna una respuesta generada por el modelo de IA.
    """
    try:
        # Validar que el prompt no esté vacío
        prompt = request.prompt.strip()
        if not prompt:
            raise HTTPException(status_code=400, detail="El prompt no puede estar vacío")
        
        # Generar la respuesta utilizando GeminiClient
        response_text = gemini_client.generate_response(prompt=prompt, context=request.context)

        # Retornar la respuesta estructurada
        return ChatResponse(success=True, prompt=prompt, response=response_text)
    
    except HTTPException as http_err:
        raise http_err  # Re-lanzar errores HTTP controlados
    
    except Exception as e:
        # Capturar errores inesperados y registrar el mensaje
        error_message = f"Error interno al procesar la solicitud: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
