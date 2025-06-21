from sqlmodel import Field
from typing import Optional
from app.db.base import BaseModel

class CyclePhaseInfos(BaseModel, table=True):
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = Field(default=None)
    tips: Optional[str] = Field(default=None)
    recommended_foods: Optional[str] = Field(default=None, max_length=3000)
    exercise_notes: Optional[str] = Field(default=None, max_length=3000)
    calorie_tips: Optional[str] = Field(default=None, max_length=3000)

    # Approximate hormone levels (arbitrary scale: e.g. 0–100)
    lh: Optional[float] = Field(default=None)
    fsh: Optional[float] = Field(default=None)
    estrogen: Optional[float] = Field(default=None)
    progesterone: Optional[float] = Field(default=None)
    androgen: Optional[float] = Field(default=None)
    insulin: Optional[float] = Field(default=None)
    prolactin: Optional[float] = Field(default=None)
    testosterone: Optional[float] = Field(default=None)
    cortisol: Optional[float] = Field(default=None)
    light_mode_colour: str = Field(default=None)
    dark_mode_colour: str = Field(default=None)