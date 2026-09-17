import os
import uuid
import random
from PIL import Image
from sqlalchemy.orm import Session
from app.models.analysis import DiseaseAnalysis
from app.utils.rules import DISEASE_KNOWLEDGE_BASE
from app.config import settings

class DiseaseDetectionService:
    async def analyze_crop_image(self, file, crop: str, farm_id: int, db: Session) -> dict:
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)

        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)

        # Basic PIL verification
        try:
            with Image.open(filepath) as img:
                img.verify()
        except Exception:
            raise ValueError("Uploaded file is not a valid or supported image.")

        mode = "demo"
        if settings.DISEASE_AI_MODE == "ai" and settings.AI_API_KEY:
            # Placeholder for AI execution path
            mode = "ai"

        pool = DISEASE_KNOWLEDGE_BASE.get(crop, DISEASE_KNOWLEDGE_BASE["Default"])
        selected = random.choice(pool)

        analysis = DiseaseAnalysis(
            farm_id=farm_id,
            image_path=filepath,
            crop=crop,
            disease=selected["disease"],
            confidence=selected["confidence"],
            severity=selected["severity"],
            recommendation=selected["recommendation"]
        )
        db.add(analysis)
        db.commit()

        return {
            "crop": crop,
            "disease": selected["disease"],
            "confidence": selected["confidence"],
            "severity": selected["severity"],
            "recommendation": selected["recommendation"],
            "mode": mode
        }