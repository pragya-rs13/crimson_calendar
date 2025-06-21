from pydantic import BaseModel
from typing import Optional
from .cycle_api_models import CycleResponse
from .period_history_api_models import PeriodHistoryResponse
    
class DashboardResponse(BaseModel):
    username: str
    current_age: int
    dob: str
    current_weight: str
    current_height: str
    current_bmi: str
    ongoing_mens: bool
    cycles: list[CycleResponse]
    period_histories: list[PeriodHistoryResponse]
    