from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.core.core_api_schema.pagination_api_models import PaginationMeta

class PeriodHistoryUpdateRequest(BaseModel):
    id: int
    start_date: Optional[date]
    end_date: Optional[date]

class PeriodHistoryResponse(BaseModel):
    id: int
    start_date: date
    end_date: Optional[date]
    is_prediction: bool
    is_ongoing: bool

class PeriodHistoryPaginatedResponse(BaseModel):
    pagination: PaginationMeta
    histories: List[PeriodHistoryResponse]

class PeriodHistoryListResponse(BaseModel):
    period_histories: List[PeriodHistoryResponse]
