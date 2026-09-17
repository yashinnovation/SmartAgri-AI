from pydantic import BaseModel, Field
from typing import Dict

class SoilAnalysisRequest(BaseModel):
    farm_id: int
    nitrogen: float = Field(..., ge=0)
    phosphorus: float = Field(..., ge=0)
    potassium: float = Field(..., ge=0)
    ph: float = Field(..., ge=0, le=14)

class ParamStatus(BaseModel):
    status: str

class SoilAnalysisResponse(BaseModel):
    health_status: str
    score: int
    parameters: Dict[str, ParamStatus]
    recommendation: str