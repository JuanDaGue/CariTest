from api.schemas.base import BaseResponse
from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    context: str = None


class ChatResponse(BaseResponse):
    prompt: str
    response: str
