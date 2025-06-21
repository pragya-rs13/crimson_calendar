from fastapi import Depends
from app.core.auth.usecases.login import LoginUseCase
from app.core.auth.rest_schema.login_api_models import LoginRequest, LoginResponse
from fastapi import HTTPException
from app.core.auth.usecases.refresh_token import RefreshTokenUseCase
from typing import TYPE_CHECKING

from app.core.auth.rest_schema.refresh_token_api_models import RefreshRequest, RefreshResponse

if TYPE_CHECKING:
    from app.core.models.user_schema import Users


class AuthService:
    def __init__(self, login_usecase: LoginUseCase = Depends(), refresh_usecase: RefreshTokenUseCase = Depends()):
        self.login_usecase = login_usecase
        self.refresh_usecase = refresh_usecase

    def login(self, request: LoginRequest) -> LoginResponse:
        user: Users = self.login_usecase.execute(request.username, request.password)

        # You can apply any mapping here before returning
        return LoginResponse(
            message="Success",
            error_code=None,
            username=user.username,
            last_login_at=user.last_login_at.isoformat() if user.last_login_at else "",
            ongoing_menses=user.profile.ongoing_mens if user.profile else False,
            is_profile_populated=bool(user.profile and user.profile.average_cycle_duration and user.profile.avg_mens_duration)
        )
        
    def refresh_token(self, request: RefreshRequest, refresh_token: str, new_token: str) -> RefreshResponse:
        user: Users = self.refresh_usecase.execute(
            username=request.username,
            refresh_token=refresh_token,
            new_token=new_token
            )
        
        if user:
            return RefreshResponse(
                message="Success",
                error_code=None
            )
        
        raise HTTPException(status_code=403, detail="Invalid Token")
