from pydantic import BaseModel
from datetime import date
from app.core.core_api_schema.pagination_api_models import PaginationMeta

class CycleUpdateRequest(BaseModel):
    id: int
    cycle_end_date: date
    cycle_length: int
    is_prediction: bool

class CycleResponse(BaseModel):
    id: int
    
    
    cycle_start_date: date
    cycle_end_date: date
    cycle_length: int
    is_prediction: bool
    
    # Phase durations
    menstrual_start: date
    menstrual_end: date
    follicular_start: date
    follicular_end: date
    ovulation_start: date
    ovulation_end: date
    luteal_start: date
    luteal_end: date
    
class CycleListResponse(BaseModel):
    cycles: list[CycleResponse]
    
class CyclePaginatedResponse(BaseModel):
    page: PaginationMeta
    cycles: list[CycleResponse]
