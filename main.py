from fastapi import FastAPI
from api.routes import faq, history ###, chat
from config.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Registrar rutas
app.include_router(faq.router, prefix="/faq", tags=["FAQ"])
app.include_router(history.router, prefix="/history", tags=["History"])
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])
