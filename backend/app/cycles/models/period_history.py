from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

from app.db.base import BaseModel

if TYPE_CHECKING:
    from .cycles import Cycles

class PeriodHistories(BaseModel, table=True):
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    start_date: date = Field(nullable=False)
    end_date: Optional[date] = Field(default=None)
    is_prediction: bool = Field(default=False, nullable=False)
    is_ongoing: bool = Field(default=True, nullable=False)

    cycle: Optional["Cycles"] = Relationship(back_populates="period")