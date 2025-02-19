from datetime import datetime
from pydantic import BaseModel

class HistoryResponse(BaseModel):
    timestamp: datetime
    query: str
    suggestion: str
    confidence: float
    matched_question: str