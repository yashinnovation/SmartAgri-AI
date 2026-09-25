from pydantic import BaseModel


class DiseaseAnalysisResponse(BaseModel):
    crop: str
    disease: str
    confidence: float
    severity: str
    recommendation: str
    mode: str
    inference_latency_ms: float
    class_index: int