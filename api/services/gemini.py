import requests
from typing import Optional
from fastapi import HTTPException
from config.config import settings


class GeminiClient:
    def __init__(self):
        """Inicializa el cliente de la API de Gemini."""
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.api_key = settings.GEMINI_API_KEY
        self.timeout = 10  # Tiempo de espera en segundos para las solicitudes

    def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Genera una respuesta utilizando la API de Gemini.

        Args:
            prompt (str): Entrada de texto principal.
            context (Optional[str]): Contexto adicional para la generación de texto.
            temperature (float): Parámetro para controlar la creatividad del modelo.
            max_tokens (int): Número máximo de tokens en la respuesta.

        Returns:
            str: Respuesta generada por el modelo.

        Raises:
            HTTPException: Si ocurre un error en la solicitud o en la respuesta de la API.
        """
        if not prompt.strip():
            raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")

        headers = {
            "Content-Type": "application/json",
        }

        # Construir el prompt final con contexto si está presente
        full_prompt = f"{context.strip()}\n\n{prompt.strip()}" if context else prompt.strip()

        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()  # Lanza un error si el código HTTP es 4xx o 5xx

            # Extraer la respuesta de manera segura
            response_data = response.json()
            candidates = response_data.get("candidates", [])
            if not candidates:
                raise HTTPException(status_code=500, detail="La API no devolvió ninguna respuesta válida.")

            content_parts = candidates[0].get("content", {}).get("parts", [])
            if not content_parts:
                raise HTTPException(status_code=500, detail="No se encontró contenido en la respuesta de la API.")

            return content_parts[0].get("text", "No se pudo generar una respuesta.")

        except requests.exceptions.Timeout:
            raise HTTPException(status_code=504, detail="Tiempo de espera agotado al conectar con la API de Gemini.")
        except requests.exceptions.ConnectionError:
            raise HTTPException(status_code=503, detail="Error de conexión con la API de Gemini.")
        except requests.exceptions.HTTPError as e:
            raise HTTPException(status_code=response.status_code, detail=f"Error HTTP: {str(e)}")
        except (KeyError, IndexError) as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta de la API: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
