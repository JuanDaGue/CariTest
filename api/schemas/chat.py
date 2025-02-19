from api.schemas.base import BaseResponse

class ChatRequest(BaseModel):
    prompt: str
    context: str = None

class ChatResponse(BaseResponse):
    prompt: str
    response: str