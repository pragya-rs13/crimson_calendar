from fastapi import FastAPI
from app.configs.settings import settings
from app.configs.cors import add_cors
from app.api.v1.api import api_router
from app.core.exceptions.global_exception_handler import setup_exception_handlers

def create_application() -> FastAPI:
    app = FastAPI(
        title="Crimson Calendar",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    add_cors(app)  # CORS
    setup_exception_handlers(app) # Global exception handling
    app.include_router(api_router, prefix="/api/v1")
    
    return app

app = create_application()