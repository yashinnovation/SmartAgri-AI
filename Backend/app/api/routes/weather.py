from fastapi import APIRouter, HTTPException
from app.schemas.weather import WeatherResponse
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])
weather_service = WeatherService()

@router.get("", response_model=WeatherResponse, summary="Get Live or Demo Weather Intelligence")
async def get_weather(location: str = "Pune"):
    try:
        return await weather_service.get_weather(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))