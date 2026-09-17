import httpx
from app.config import settings

class WeatherService:
    async def get_weather(self, location: str) -> dict:
        if settings.WEATHER_API_KEY:
            try:
                async with httpx.AsyncClient() as client:
                    url = f"http://api.weatherapi.com/v1/forecast.json?key={settings.WEATHER_API_KEY}&q={location}&days=3"
                    resp = await client.get(url, timeout=5.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        curr = data["current"]
                        forecast_day = data["forecast"]["forecastday"][0]["day"]
                        return {
                            "location": data["location"]["name"],
                            "current": {
                                "temperature": float(curr["temp_c"]),
                                "humidity": float(curr["humidity"]),
                                "wind_speed": float(curr["wind_kph"]),
                                "rain_probability": float(forecast_day.get("daily_chance_of_rain", 20)),
                                "condition": curr["condition"]["text"]
                            },
                            "forecast": [
                                {
                                    "day": "Today",
                                    "temperature": float(forecast_day["maxtemp_c"]),
                                    "rain_probability": float(forecast_day.get("daily_chance_of_rain", 20))
                                }
                            ],
                            "farming_advice": "Live weather conditions retrieved. Adjust irrigation accordingly.",
                            "mode": "live"
                        }
            except Exception:
                pass  # Fall back to demo safely

        return {
            "location": location or "Pune",
            "current": {
                "temperature": 31.0,
                "humidity": 68.0,
                "wind_speed": 14.0,
                "rain_probability": 20.0,
                "condition": "Partly Cloudy"
            },
            "forecast": [
                {"day": "Today", "temperature": 31.0, "rain_probability": 20.0},
                {"day": "Tomorrow", "temperature": 32.0, "rain_probability": 10.0},
                {"day": "Day After", "temperature": 30.0, "rain_probability": 40.0}
            ],
            "farming_advice": "Favorable farming conditions today. Low risk of immediate heavy precipitation.",
            "mode": "demo"
        }