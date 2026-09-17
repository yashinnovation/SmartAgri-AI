from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
analytics_service = AnalyticsService()

@router.get("/{farm_id}", summary="Get Historical Analytics Charts Data")
def get_analytics(farm_id: int, db: Session = Depends(get_db)):
    try:
        return analytics_service.get_analytics(farm_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))