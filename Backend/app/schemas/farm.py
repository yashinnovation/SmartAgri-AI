from pydantic import BaseModel
from datetime import datetime

class FarmBase(BaseModel):
    farm_name: str
    location: str
    area: float
    soil_type: str
    crop_type: str

class FarmCreate(FarmBase):
    user_id: int = 1

class FarmUpdate(BaseModel):
    farm_name: str | None = None
    location: str | None = None
    area: float | None = None
    soil_type: str | None = None
    crop_type: str | None = None

class FarmResponse(FarmBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True