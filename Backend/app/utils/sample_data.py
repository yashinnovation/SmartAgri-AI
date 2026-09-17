from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User
from app.models.farm import Farm
from app.models.analysis import FarmActivity, SoilAnalysis, IrrigationAnalysis

def init_demo_data(db: Session):
    user = db.query(User).filter_by(id=1).first()
    if not user:
        user = User(id=1, name="Farmer Demo", email="demo@agrismart.ai")
        db.add(user)
        db.commit()

    farm = db.query(Farm).filter_by(id=1).first()
    if not farm:
        farm = Farm(
            id=1,
            user_id=1,
            farm_name="AgriSmart Demo Farm",
            location="Pune",
            area=5.0,
            soil_type="Loamy",
            crop_type="Tomato"
        )
        db.add(farm)
        db.commit()

        # Add initial soil record
        soil = SoilAnalysis(
            farm_id=1,
            nitrogen=78,
            phosphorus=42,
            potassium=65,
            ph=6.8,
            health_status="Good",
            recommendation="Soil is well nourished. Maintain current organic fertilizer rotation."
        )
        db.add(soil)

        # Add initial irrigation record
        irr = IrrigationAnalysis(
            farm_id=1,
            soil_moisture=38.0,
            temperature=31.0,
            humidity=55.0,
            rain_probability=20.0,
            recommendation="Moderate irrigation recommended",
            amount="12-15 litres/m²",
            best_time="Early morning",
            reason="Low soil moisture combined with warm temperatures."
        )
        db.add(irr)

        # Populate analytics historical records
        base_date = datetime.utcnow() - timedelta(days=3)
        health_vals = [78.0, 80.0, 83.0, 85.0]
        moisture_vals = [44.0, 41.0, 39.0, 38.0]

        for i in range(4):
            record_date = base_date + timedelta(days=i)
            db.add(FarmActivity(farm_id=1, metric="crop_health", value=health_vals[i], recorded_at=record_date))
            db.add(FarmActivity(farm_id=1, metric="soil_moisture", value=moisture_vals[i], recorded_at=record_date))

        db.commit()