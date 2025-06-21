from app.core.repo.user_repo import UserRepository
from app.core.repo.profile_repo import ProfileRepository
from fastapi import HTTPException, Response, Depends
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.core.models.user_schema import Users


class LoginUseCase:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository.with_session), profile_repo: ProfileRepository = Depends(ProfileRepository.with_session)):
        self.user_repo = user_repo
        self.profile_repo = profile_repo

    def execute(self, username: str, password: str):
        user: Users = self.user_repo.get_by_username(username)
        if not user or not user.verify_password(password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if user.last_login_at is None or user.profile is None:
            self.profile_repo.create_profile_for_user(user_id=user.id)
            
        self.user_repo.update_last_login(user)

        return user
