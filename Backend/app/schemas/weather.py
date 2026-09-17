from pydantic import BaseModel
from typing import List

class CurrentWeather(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    rain_probability: float
    condition: str

class WeatherForecast(BaseModel):
    day: str
    temperature: float
    rain_probability: float

class WeatherResponse(BaseModel):
    location: str
    current: CurrentWeather
    forecast: List[WeatherForecast]
    farming_advice: str
    mode: str