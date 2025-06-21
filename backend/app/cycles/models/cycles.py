from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

from app.db.base import BaseModel

if TYPE_CHECKING:
    from .period_history import PeriodHistories

class Cycles(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    period_id: Optional[int] = Field(foreign_key="periodhistories.id", nullable=True)
    
    cycle_start_date: date = Field(nullable=False)
    cycle_end_date: Optional[date] = Field(default=None)
    cycle_length: Optional[int] = Field(default=None)  # in days
    
    # Phase durations
    menstrual_start: Optional[date] = None
    menstrual_end: Optional[date] = None
    follicular_start: Optional[date] = None
    follicular_end: Optional[date] = None
    ovulation_start: Optional[date] = None
    ovulation_end: Optional[date] = None
    luteal_start: Optional[date] = None
    luteal_end: Optional[date] = None

    is_prediction: bool = Field(default=False)

    period: Optional["PeriodHistories"] = Relationship(back_populates="cycle")