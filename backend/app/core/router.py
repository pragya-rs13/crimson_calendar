from fastapi import APIRouter, Response, Depends
from app.core.auth.service import login_user
from app.security.dependency import get_current_user
from app.core.models.login import LoginRequest

core_router = APIRouter()

@core_router.post("/login")
def login(response: Response, loginRequest: LoginRequest):
    return login_user(loginRequest.username, loginRequest.password, response)


# ONLY USED FOR TESTING, REMOVE!!

@core_router.get("/dashboard")
def dashboard_endpoint(current_user: dict = Depends(get_current_user)):
    return {"message": "Accessed dashboard successfully", "user": current_user}