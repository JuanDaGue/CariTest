from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import faq, history, chat
from fastapi.responses import JSONResponse
from config.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestionar preguntas frecuentes (FAQ), historial y chat.",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a los dominios permitidos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(faq.router, prefix="/faq", tags=["FAQ"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

# Manejo global de excepciones
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Ocurrió un error interno. Contacta al soporte."},
    )
