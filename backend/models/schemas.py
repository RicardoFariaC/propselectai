from pydantic import BaseModel
from typing import Optional, List

class PropellerRequest(BaseModel):
    weight_kg: float
    engine_power_hp: float
    cruise_speed_ms: float
    mission_type: str
    max_diameter_inches: Optional[float] = None

class PropellerResponse(BaseModel):
    name: str
    diameter: float
    pitch: float
    efficiency: float
    thrust: float
    justification: str

class RecommendationResponse(BaseModel):
    recommendations: List[PropellerResponse]
    report_path: Optional[str] = None
    references: Optional[List[str]] = None

