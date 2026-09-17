from fastapi import APIRouter, HTTPException
from app.schemas.crop import CropRecommendRequest, CropRecommendResponse
from app.services.crop_service import CropRecommendationService

router = APIRouter(prefix="/crops", tags=["Crop Recommendation"])
crop_service = CropRecommendationService()

@router.post("/recommend", response_model=CropRecommendResponse, summary="Recommend Ideal Crops")
def recommend_crops(payload: CropRecommendRequest):
    try:
        recommendations = crop_service.recommend(
            soil_type=payload.soil_type,
            ph=payload.ph,
            n=payload.nitrogen,
            p=payload.phosphorus,
            k=payload.potassium,
            temp=payload.temperature,
            humidity=payload.humidity,
            rain=payload.rainfall
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))