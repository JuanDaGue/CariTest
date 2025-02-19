from fastapi import APIRouter, HTTPException
from api.schemas.faq import FAQRequest, FAQResponse
from api.services.faq_suggest import get_suggestion
from api.services.history_manager import add_to_history

router = APIRouter()


@router.post("/suggest", response_model=FAQResponse)
async def suggest_faq(query: FAQRequest):
    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query vacía")

    suggestion = get_suggestion(query.query)
    add_to_history(query.query, suggestion)

    return FAQResponse(
        query=query.query,
        suggestion=suggestion["response"],  # Acceder como diccionario
        confidence=suggestion["confidence"]
    )
