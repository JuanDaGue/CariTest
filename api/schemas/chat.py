from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    context: str = None


class ChatResponse(BaseModel):
    success: bool
    prompt: str
    response: str
    error: str = None