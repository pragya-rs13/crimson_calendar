from pydantic import BaseModel
from typing import Optional

class RefreshRequest(BaseModel):
    username: str
    
class RefreshResponse(BaseModel):
    message: str
    error_code: Optional[str]