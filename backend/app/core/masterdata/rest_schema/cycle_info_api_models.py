from pydantic import BaseModel
    
class CycleInfoResponse(BaseModel):
    name: str
    description: str
    tips: str
    recommended_foods: str
    exercise_notes: str
    calorie_tips: str

    # approx hormone levels (scale: 0–100)
    lh: float
    fsh: float
    estrogen: float
    progesterone: float
    androgen: float
    insulin: float
    prolactin: float
    testosterone: float
    cortisol: float
    
    # UI help
    light_mode_colour: str
    dark_mode_colour: str
    
class CycleInfoListResponse(BaseModel):
    phase_info: list[CycleInfoResponse]
    
    
    