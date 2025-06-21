from jose import ExpiredSignatureError, JWTError
from app.core.repo.user_repo import UserRepository
from app.core.repo.profile_repo import ProfileRepository
from fastapi import HTTPException, Depends
from app.security.auth import verify_token
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.core.models.user_schema import Users


class RefreshTokenUseCase:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository.with_session)):
        self.user_repo = user_repo

    def execute(self, username: str, refresh_token: str, new_token: str):
        user: Users = self.user_repo.get_by_username(username)
        if not user or not user.verify_refresh_token(refresh_token=refresh_token):
            raise HTTPException(status_code=403, detail="Invalid token")
        
        try:
            _ = verify_token(refresh_token)
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid Token")
        
        self.user_repo.update_refresh_token(new_token)
            
        self.user_repo.update_last_login(user)

        return user
