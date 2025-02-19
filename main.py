from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from difflib import get_close_matches
import json
from typing import List, Dict

app = FastAPI()

# Cargar base de conocimiento
with open("data/dataChat.json", "r") as f:
    faqs = json.load(f)

# Historial en memoria
history = []


class QueryRequest(BaseModel):
    query: str


def get_suggestion(query: str) -> str:
    questions = [faq["pregunta"] for faq in faqs]
    matches = get_close_matches(query, questions, n=1, cutoff=0.5)
    return next(
        (faq["respuesta"] for faq in faqs if faq["pregunta"] == matches[0]),
        "No hay sugerencias disponibles."
    ) if matches else "No hay sugerencias disponibles."


@app.post("/suggest")
async def suggest(query_request: QueryRequest):
    if not query_request.query.strip():
        raise HTTPException(status_code=400, detail="Query vacía")
    suggestion = get_suggestion(query_request.query)
    history.append({"query": query_request.query, "suggestion": suggestion})
    return {"suggestion": suggestion}


@app.get("/history")
async def get_history():
    return history


@app.post("/faq")
async def add_faq(pregunta: str, respuesta: str):
    faqs.append({"pregunta": pregunta, "respuesta": respuesta})
    return {"message": "FAQ agregada"}
