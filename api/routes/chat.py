from fastapi import APIRouter, HTTPException
from api.schemas.chat import ChatRequest, ChatResponse
from api.services.gemini import GeminiClient

router = APIRouter()
gemini_client = GeminiClient()


@router.post("/generate", response_model=ChatResponse)
async def chat_with_gemini(request: ChatRequest):
    try:
        response = gemini_client.generate_response(
            prompt=request.prompt,
            context=request.context
        )
        return ChatResponse(
            prompt=request.prompt,
            response=response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
