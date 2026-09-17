from app.utils.rules import CROP_RULES

class CropRecommendationService:
    def recommend(self, soil_type: str, ph: float, n: float, p: float, k: float, temp: float, humidity: float, rain: float) -> list:
        results = []

        for crop_name, rules in CROP_RULES.items():
            score = 100.0
            reasons = []

            # Evaluate pH range
            if not (rules["ph"][0] <= ph <= rules["ph"][1]):
                score -= 15
                reasons.append(f"pH {ph} outside ideal ({rules['ph'][0]}-{rules['ph'][1]})")

            # Evaluate Temperature
            if not (rules["temp"][0] <= temp <= rules["temp"][1]):
                score -= 15
                reasons.append(f"Temperature {temp}°C outside range ({rules['temp'][0]}-{rules['temp'][1]}°C)")

            # Evaluate Rainfall
            if not (rules["rain"][0] <= rain <= rules["rain"][1]):
                score -= 10
                reasons.append("Rainfall slightly non-optimal")

            # Evaluate Soil Type
            if soil_type not in rules["soils"]:
                score -= 20
                reasons.append(f"{soil_type} is not primary soil choice")

            score = max(30.0, score)
            reason_str = "; ".join(reasons) if reasons else "Conditions closely match crop requirements."

            results.append({
                "crop": crop_name,
                "suitability": round(score, 1),
                "reason": reason_str
            })

        results.sort(key=lambda x: x["suitability"], reverse=True)
        return results