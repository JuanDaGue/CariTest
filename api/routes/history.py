from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas.history import HistoryResponse
from api.services.history_manager import get_history, reset_history

router = APIRouter()


@router.get("/", response_model=List[HistoryResponse])
async def get_history_route(limit: int = 10):
    try:
        return get_history(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_history_route():
    try:
        reset_history()
        return {"success": True, "message": "Historial reiniciado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
