from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.disease import DiseaseAnalysisResponse
from app.services.disease_service import DiseaseDetectionService

router = APIRouter(prefix="/disease", tags=["Disease Detection"])
disease_service = DiseaseDetectionService()

@router.post("/analyze", response_model=DiseaseAnalysisResponse, summary="Analyze Crop Disease Image")
async def analyze_disease(
    crop: str = Form(...),
    farm_id: int = Form(1),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Provided file must be a valid image format.")
    try:
        return await disease_service.analyze_crop_image(image, crop, farm_id, db)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during analysis.")