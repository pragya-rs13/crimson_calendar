from fastapi import APIRouter
from app.core.router import core_router
# from app.prediction.router import prediction_router
# from app.dashboard.router import dashboard_router
# from app.charting.router import charting_router

api_router = APIRouter()

api_router.include_router(core_router, prefix="", tags=["core"])
# api_router.include_router(prediction_router, prefix="/prediction", tags=["prediction"])
# api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
# api_router.include_router(charting_router, prefix="/charting", tags=["charting"])