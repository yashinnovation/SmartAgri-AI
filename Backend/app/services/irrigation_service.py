from sqlalchemy.orm import Session
from app.models.analysis import IrrigationAnalysis

class IrrigationService:
    def calculate_recommendation(self, farm_id: int, crop: str, moisture: float, temp: float, humidity: float, rain_prob: float, db: Session) -> dict:
        if moisture < 30:
            status = "high"
            recommendation = "High irrigation required immediately"
            amount = "20-25 litres/m²"
            reason = "Critical soil moisture deficit."
        elif 30 <= moisture <= 50:
            status = "moderate"
            recommendation = "Moderate irrigation recommended"
            amount = "12-15 litres/m²"
            reason = "Low soil moisture combined with ambient temperature."
        else:
            status = "low"
            recommendation = "No immediate irrigation needed"
            amount = "0 litres/m²"
            reason = "Adequate soil moisture level maintained."

        if rain_prob > 60:
            status = "low"
            recommendation = "Postpone irrigation due to high rain probability"
            amount = "0 litres/m²"
            reason = f"Rain probability is high ({rain_prob}%)."

        best_time = "Early morning" if temp > 28 else "Late afternoon"

        analysis = IrrigationAnalysis(
            farm_id=farm_id,
            soil_moisture=moisture,
            temperature=temp,
            humidity=humidity,
            rain_probability=rain_prob,
            recommendation=recommendation,
            amount=amount,
            best_time=best_time,
            reason=reason
        )
        db.add(analysis)
        db.commit()

        return {
            "status": status,
            "recommendation": recommendation,
            "amount": amount,
            "best_time": best_time,
            "reason": reason
        }