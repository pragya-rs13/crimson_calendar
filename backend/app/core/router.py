from fastapi import APIRouter, Response, Depends
from app.core.auth.service import AuthService
from app.security.dependency import get_current_user
from app.core.auth.rest_schema.login_api_models import LoginResponse
from app.core.auth.rest_schema.login_api_models import LoginRequest
from app.security.auth import create_access_token, create_refresh_token
from app.core.auth.rest_schema.refresh_token_api_models import RefreshResponse

core_router = APIRouter()

@core_router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    response: Response,
    service: AuthService = Depends()
):
    #  (if incorrect password) You shall not pass
    result = service.login(request, response)

    #  new tokinssss
    access_token = create_access_token({"sub": result.username})
    refresh_token = create_refresh_token({"sub": result.username})

    #  here, cookies for your efforts
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax", secure=False)
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax", secure=False)
    
    #  bye
    return result


@core_router.get("/refresh-token", response_model=RefreshResponse)
def refresh_token(
    request: LoginRequest,
    response: Response,
    service: AuthService = Depends()
    ):
    # new tokennnsssss
    access_token = create_access_token({"sub": request.username})
    new_refresh_token = create_refresh_token({"sub": request.username})
    
    # verify or kil
    result = service.refresh_token(
        request=request,
        refresh_token=request.cookies.get("refresh_token", None),
        new_token=new_refresh_token,
        )
    
    # set coomkies
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax", secure=False)
    response.set_cookie("refresh_token", new_refresh_token, httponly=True, samesite="lax", secure=False)
    
    #  bye bye
    return result