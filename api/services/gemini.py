import requests
from typing import Optional
from fastapi import HTTPException
from config.config import settings


class GeminiClient:
    def __init__(self):
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.api_key = settings.GEMINI_API_KEY

    def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        headers = {
            "Content-Type": "application/json",
        }
        
        # Construir el prompt completo
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
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
                timeout=10
            )
            
            response.raise_for_status()
            
            # Extraer la respuesta
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error en la API de Gemini: {str(e)}"
            )
        except (KeyError, IndexError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error procesando la respuesta de Gemini: {str(e)}"
            )