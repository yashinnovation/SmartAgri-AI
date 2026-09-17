from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
dashboard_service = DashboardService()

@router.get("/{farm_id}", summary="Get Farm Dashboard Summary")
async def get_dashboard(farm_id: int, db: Session = Depends(get_db)):
    try:
        return await dashboard_service.get_dashboard_data(farm_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))