from sqlalchemy.orm import Session
from app.models.farm import Farm
from app.models.analysis import SoilAnalysis, IrrigationAnalysis, DiseaseAnalysis
from app.services.analytics_service import AnalyticsService
from app.services.weather_service import WeatherService

class DashboardService:
    def __init__(self):
        self.analytics_service = AnalyticsService()
        self.weather_service = WeatherService()

    async def get_dashboard_data(self, farm_id: int, db: Session) -> dict:
        farm = db.query(Farm).filter_by(id=farm_id).first()
        farm_name = farm.farm_name if farm else "Demo Farm"
        crop = farm.crop_type if farm else "Tomato"
        area = farm.area if farm else 5.0
        location = farm.location if farm else "Pune"

        weather = await self.weather_service.get_weather(location)
        latest_irr = db.query(IrrigationAnalysis).filter_by(farm_id=farm_id).order_by(IrrigationAnalysis.created_at.desc()).first()

        moisture = latest_irr.soil_moisture if latest_irr else 38.0
        temp = weather["current"]["temperature"]
        rain_prob = weather["current"]["rain_probability"]

        charts_data = self.analytics_service.get_analytics(farm_id, db)

        return {
            "farm": {
                "name": farm_name,
                "crop": crop,
                "area": area
            },
            "summary": {
                "crop_health": 85,
                "soil_moisture": moisture,
                "temperature": temp,
                "rain_probability": rain_prob
            },
            "recommendations": [
                {
                    "type": "irrigation",
                    "title": "Irrigation",
                    "message": latest_irr.recommendation if latest_irr else "Moderate irrigation recommended today."
                },
                {
                    "type": "crop_health",
                    "title": "Crop Health",
                    "message": "Crop health is stable."
                },
                {
                    "type": "weather",
                    "title": "Weather",
                    "message": weather["farming_advice"]
                }
            ],
            "alerts": [
                "Soil moisture is slightly low" if moisture < 40 else "Optimal field conditions"
            ],
            "charts": {
                "crop_health": charts_data["crop_health"],
                "farm_condition": charts_data["soil_moisture"]
            }
        }