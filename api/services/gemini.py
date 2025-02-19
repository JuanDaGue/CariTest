import google.generativeai as genai
from config.config import settings


class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, prompt: str, context: str = None) -> str:
        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        response = self.model.generate_content(
            contents=full_prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )
        return response.text
