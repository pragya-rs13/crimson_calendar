from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str
    
class LoginResponse(BaseModel):
    message: str
    error_code: Optional[str]
    username: str
    last_login_at: str
    ongoing_menses: bool
    is_profile_populated: bool
