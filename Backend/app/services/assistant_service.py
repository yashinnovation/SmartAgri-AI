import httpx
from sqlalchemy.orm import Session
from app.models.farm import Farm
from app.models.analysis import DiseaseAnalysis, SoilAnalysis, IrrigationAnalysis
from app.config import settings

SYSTEM_INSTRUCTION = """You are AgriSmart AI, an agricultural guidance assistant.
Provide practical, easy-to-understand farming guidance.
Use the provided farm context.
Do not pretend to be certain when information is uncertain.
For serious crop disease or chemical treatment questions, recommend consulting a qualified agricultural expert."""

class AssistantService:
    async def chat(self, message: str, farm_id: int, db: Session) -> dict:
        farm = db.query(Farm).filter_by(id=farm_id).first()
        latest_disease = db.query(DiseaseAnalysis).filter_by(farm_id=farm_id).order_by(DiseaseAnalysis.created_at.desc()).first()
        latest_soil = db.query(SoilAnalysis).filter_by(farm_id=farm_id).order_by(SoilAnalysis.created_at.desc()).first()
        latest_irr = db.query(IrrigationAnalysis).filter_by(farm_id=farm_id).order_by(IrrigationAnalysis.created_at.desc()).first()

        context = {
            "crop": farm.crop_type if farm else "Unknown",
            "soil_type": farm.soil_type if farm else "Unknown",
            "latest_disease": latest_disease.disease if latest_disease else "None reported",
            "soil_ph": latest_soil.ph if latest_soil else "N/A",
            "soil_moisture": latest_irr.soil_moisture if latest_irr else "N/A"
        }

        if settings.AI_API_KEY and settings.AI_PROVIDER == "gemini":
            try:
                prompt_text = f"{SYSTEM_INSTRUCTION}\nContext: {context}\nUser Question: {message}"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.AI_API_KEY}"
                payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
                
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json=payload, timeout=8.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        reply = data["candidates"][0]["content"]["parts"][0]["text"]
                        return {"reply": reply, "context_used": context}
            except Exception:
                pass  # Fallback gracefully to offline rule-engine answers

        # Rule-based agricultural reasoning fallback
        msg_lower = message.lower()
        if "yellow" in msg_lower or "disease" in msg_lower or "spot" in msg_lower:
            reply = f"Yellowing leaves on {context['crop']} often indicate Nitrogen deficiency or early fungal infection like Blight. Check soil pH (Current: {context['soil_ph']}) and inspect leaf undersides for spores. Avoid overwatering."
        elif "water" in msg_lower or "irrigation" in msg_lower:
            reply = f"For {context['crop']} in {context['soil_type']} soil, irrigate when surface soil feels dry. Current moisture level is around {context['soil_moisture']}%. Water near roots early in the morning."
        elif "soil" in msg_lower or "fertilizer" in msg_lower:
            reply = f"Your soil type is registered as {context['soil_type']}. Maintain balanced N-P-K nutrient application and ensure soil pH remains near optimal level (~6.5)."
        else:
            reply = f"Regarding {context['crop']}: Ensure proper weed control, maintain adequate spacing for aeration, and keep soil moisture balanced based on local ambient heat."

        return {"reply": reply, "context_used": context}