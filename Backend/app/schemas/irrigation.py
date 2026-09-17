from pydantic import BaseModel, Field

class IrrigationRequest(BaseModel):
    farm_id: int
    crop: str
    soil_moisture: float = Field(..., ge=0, le=100)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    rain_probability: float = Field(..., ge=0, le=100)

class IrrigationResponse(BaseModel):
    status: str
    recommendation: str
    amount: str
    best_time: str
    reason: str