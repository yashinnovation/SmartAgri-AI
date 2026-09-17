from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.soil import SoilAnalysisRequest, SoilAnalysisResponse
from app.services.soil_service import SoilService

router = APIRouter(prefix="/soil", tags=["Soil"])
soil_service = SoilService()

@router.post("/analyze", response_model=SoilAnalysisResponse, summary="Analyze Soil NPK and pH Health")
def analyze_soil(payload: SoilAnalysisRequest, db: Session = Depends(get_db)):
    try:
        return soil_service.analyze(
            farm_id=payload.farm_id,
            n=payload.nitrogen,
            p=payload.phosphorus,
            k=payload.potassium,
            ph=payload.ph,
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))