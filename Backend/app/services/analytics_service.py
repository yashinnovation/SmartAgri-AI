from sqlalchemy.orm import Session
from app.models.analysis import FarmActivity

class AnalyticsService:
    def get_analytics(self, farm_id: int, db: Session) -> dict:
        activities = db.query(FarmActivity).filter_by(farm_id=farm_id).order_by(FarmActivity.recorded_at.asc()).all()

        health_records = []
        moisture_records = []

        for act in activities:
            dt_str = act.recorded_at.strftime("%Y-%m-%d")
            if act.metric == "crop_health":
                health_records.append({"date": dt_str, "value": act.value})
            elif act.metric == "soil_moisture":
                moisture_records.append({"date": dt_str, "value": act.value})

        return {
            "crop_health": health_records,
            "soil_moisture": moisture_records
        }