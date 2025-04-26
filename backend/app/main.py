from fastapi import FastAPI
from app.configs.settings import settings
from app.configs.cors import add_cors
from app.api.v1.api import api_router

def create_application() -> FastAPI:
    app = FastAPI(
        title="Crimson Calendar",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    add_cors(app)  # CORS
    app.include_router(api_router, prefix="/api/v1")
    
    return app

app = create_application()