from app.db.base import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime, timezone


if TYPE_CHECKING:
    from app.core.models.user_schema import Users

class Profiles(BaseModel, table=True):
    user_id: int = Field(
        foreign_key="users.id",
        nullable=False,
        ondelete="CASCADE",
        index=True,
        unique=True,  # enforce one-to-one 
    )
    current_weight: Optional[int] = Field(nullable=True, default=None)
    current_height: Optional[int] = Field(nullable=True, default=None)
    date_of_birth: Optional[date] = Field(nullable=True, default=None)
    ongoing_mens: Optional[bool] = Field(nullable=True, default=False)
    avg_mens_duration: Optional[int] = Field(nullable=True, default=5)
    average_cycle_duration: Optional[int] = Field(default=27, nullable=False)
    
    user: Optional["Users"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={
            "lazy": "joined"  # optional, not strictly needed both sides
        }
    )
    
    @property
    def age(self) -> Optional[int]:
        if not self.date_of_birth:
            return None
        # Use UTC-safe today's date
        today = datetime.now(timezone.utc).date()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @property
    def bmi(self) -> Optional[float]:
        if not self.current_height or not self.current_weight:
            return None
        height_m = self.current_height / 100 
        return round(self.current_weight / (height_m ** 2), 2)
