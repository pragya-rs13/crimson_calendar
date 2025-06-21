from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class TimestampMixin(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

class IDMixin(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

# Base class for all models
class BaseModel(TimestampMixin, IDMixin, SQLModel):
    pass
