from sqlalchemy.orm import Session
from app.models.analysis import SoilAnalysis

class SoilService:
    def analyze(self, farm_id: int, n: float, p: float, k: float, ph: float, db: Session) -> dict:
        score = 100
        params = {}

        # Nitrogen logic
        if n < 50:
            params["nitrogen"] = {"status": "Low"}
            score -= 15
        elif n > 110:
            params["nitrogen"] = {"status": "High"}
            score -= 10
        else:
            params["nitrogen"] = {"status": "Good"}

        # Phosphorus logic
        if p < 30:
            params["phosphorus"] = {"status": "Low"}
            score -= 15
        elif p > 70:
            params["phosphorus"] = {"status": "High"}
            score -= 10
        else:
            params["phosphorus"] = {"status": "Moderate" if p < 45 else "Good"}

        # Potassium logic
        if k < 30:
            params["potassium"] = {"status": "Low"}
            score -= 15
        else:
            params["potassium"] = {"status": "Good"}

        # pH logic
        if 6.0 <= ph <= 7.2:
            params["ph"] = {"status": "Optimal"}
        else:
            params["ph"] = {"status": "Sub-optimal"}
            score -= 15

        health_status = "Excellent" if score >= 85 else "Good" if score >= 70 else "Needs Attention"
        recommendation = "Soil parameters are well balanced." if score >= 80 else "Add organic compost and balance NPK application."

        analysis = SoilAnalysis(
            farm_id=farm_id,
            nitrogen=n,
            phosphorus=p,
            potassium=k,
            ph=ph,
            health_status=health_status,
            recommendation=recommendation
        )
        db.add(analysis)
        db.commit()

        return {
            "health_status": health_status,
            "score": max(score, 0),
            "parameters": params,
            "recommendation": recommendation
        }