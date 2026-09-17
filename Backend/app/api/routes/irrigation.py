from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.irrigation import IrrigationRequest, IrrigationResponse
from app.services.irrigation_service import IrrigationService

router = APIRouter(prefix="/irrigation", tags=["Irrigation"])
irrigation_service = IrrigationService()

@router.post("/recommend", response_model=IrrigationResponse, summary="Calculate Smart Irrigation Schedule")
def recommend_irrigation(payload: IrrigationRequest, db: Session = Depends(get_db)):
    try:
        return irrigation_service.calculate_recommendation(
            farm_id=payload.farm_id,
            crop=payload.crop,
            moisture=payload.soil_moisture,
            temp=payload.temperature,
            humidity=payload.humidity,
            rain_prob=payload.rain_probability,
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))