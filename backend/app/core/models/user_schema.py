from app.db.base import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.security.hashing import verify_password

if TYPE_CHECKING:
    from app.core.models.profile_schema import Profiles

class Users(BaseModel, table=True):
    username: str = Field(nullable=False, max_length=255, unique=True)
    email: str = Field(nullable=False, max_length=255, unique=True)
    password: str = Field(nullable=False, max_length=255)
    refresh_token: Optional[str] = Field(nullable=True, default=None)
    last_login_at: Optional[datetime] = Field(nullable=True, default=None)
    profile: Optional["Profiles"] = Relationship(
    back_populates="user",
    sa_relationship_kwargs={
        "lazy": "joined",
        "cascade": "all, delete-orphan",  # <-- ORM cascade behavior
        "uselist": False
    }
)
    
    def verify_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.password)
    
    def verify_refresh_token(self, refresh_token: str) -> bool:
        return refresh_token == self.refresh_token
