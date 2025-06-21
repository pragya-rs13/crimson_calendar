from fastapi import Depends
from sqlmodel import Session
from app.core.models.user_schema import Users as User
from app.db.base_repository import BaseRepository
from datetime import datetime, timezone

from app.db.session import get_session

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.user_query = self.db.query(User)
        
    @classmethod
    def with_session(cls, db: Session = Depends(get_session)):
        return cls(db)

    def get_by_username(self, username: str) -> User | None:
        return self.user_query.filter(User.username == username).first()

    def update_last_login(self, user: User):
        user.last_login_at = datetime.now(timezone.utc)
        self.db.add(user)
        self.db.commit()

    def save_refresh_token(self, user: User, refresh_token: str):
        user.refresh_token = refresh_token
        self.db.add(user)
        self.db.commit()