import os
import uuid

from PIL import Image
from sqlalchemy.orm import Session

from app.models.analysis import DiseaseAnalysis
from app.utils.rules import DISEASE_KNOWLEDGE_BASE
from app.config import settings

from ml.predictor import predict_disease


class DiseaseDetectionService:

    async def analyze_crop_image(
        self,
        file,
        crop: str,
        farm_id: int,
        db: Session
    ) -> dict:

        # ---------------------------------------
        # Save uploaded image
        # ---------------------------------------

        ext = (
            file.filename.split(".")[-1].lower()
            if "." in file.filename
            else "jpg"
        )

        filename = f"{uuid.uuid4().hex}.{ext}"

        filepath = os.path.join(
            settings.UPLOAD_DIR,
            filename
        )

        contents = await file.read()

        with open(filepath, "wb") as f:
            f.write(contents)

        # ---------------------------------------
        # Verify image
        # ---------------------------------------

        try:
            with Image.open(filepath) as img:
                img.verify()
        except Exception:
            raise ValueError(
                "Uploaded file is not a valid or supported image."
            )

        # ---------------------------------------
        # Open image for ML prediction
        # ---------------------------------------

        try:
            image = Image.open(filepath).convert("RGB")
        except Exception:
            raise ValueError(
                "Could not read the uploaded image."
            )

        # ---------------------------------------
        # REAL ML PREDICTION
        # ---------------------------------------

        prediction = predict_disease(image)

        model_disease = prediction["disease"]
        confidence = prediction["confidence"]
        latency_ms = prediction["latency_ms"]
        class_index = prediction["class_index"]

        # ---------------------------------------
        # Convert model label to readable name
        # ---------------------------------------

        disease_name = model_disease.replace("___", " - ")
        disease_name = disease_name.replace("_", " ")

        # ---------------------------------------
        # Find existing disease information
        # ---------------------------------------

        selected = None

        crop_pool = DISEASE_KNOWLEDGE_BASE.get(
            crop,
            []
        )

        for item in crop_pool:

            known_name = item["disease"].lower()

            if (
                known_name in disease_name.lower()
                or disease_name.lower() in known_name
            ):
                selected = item
                break

        # ---------------------------------------
        # Fallback information
        # ---------------------------------------

        if selected is None:

            selected = {
                "severity": (
                    "Low confidence"
                    if confidence < 60
                    else "Not assessed"
                ),
                "recommendation": (
                    f"The ML model predicted {disease_name} "
                    f"with {confidence:.2f}% confidence. "
                    "This result should be verified with a clear "
                    "leaf image or agricultural expert before "
                    "taking treatment action."
                )
            }

        # ---------------------------------------
        # Crop mismatch warning
        # ---------------------------------------

        crop_warning = ""

        if crop:

            predicted_crop = (
                model_disease.split("___")[0]
                .replace("_", " ")
                .strip()
                .lower()
            )

            selected_crop = crop.strip().lower()

            if (
                predicted_crop
                and predicted_crop != "healthy"
                and predicted_crop != selected_crop
            ):
                crop_warning = (
                    f" Note: the model predicted a "
                    f"{predicted_crop} image while the selected "
                    f"crop is {crop}. Please verify the image "
                    f"and crop selection."
                )

        # ---------------------------------------
        # Final recommendation
        # ---------------------------------------

        recommendation = (
            selected["recommendation"]
            + crop_warning
        )

        # ---------------------------------------
        # Save analysis to database
        # ---------------------------------------

        analysis = DiseaseAnalysis(
            farm_id=farm_id,
            image_path=filepath,
            crop=crop,
            disease=disease_name,
            confidence=confidence,
            severity=selected["severity"],
            recommendation=recommendation
        )

        db.add(analysis)
        db.commit()

        # ---------------------------------------
        # API response
        # ---------------------------------------

        return {
            "crop": crop,
            "disease": disease_name,
            "confidence": confidence,
            "severity": selected["severity"],
            "recommendation": recommendation,
            "mode": "ml",
            "inference_latency_ms": round(latency_ms, 2),
            "class_index": class_index
        }