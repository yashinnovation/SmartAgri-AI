from pydantic import BaseModel, Field
from typing import List

class CropRecommendRequest(BaseModel):
    soil_type: str
    ph: float = Field(..., ge=0, le=14)
    nitrogen: float = Field(..., ge=0)
    phosphorus: float = Field(..., ge=0)
    potassium: float = Field(..., ge=0)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    rainfall: float = Field(..., ge=0)

class CropItem(BaseModel):
    crop: str
    suitability: float
    reason: str

class CropRecommendResponse(BaseModel):
    recommendations: List[CropItem]