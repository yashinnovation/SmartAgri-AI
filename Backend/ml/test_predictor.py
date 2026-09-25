from pathlib import Path
from PIL import Image

from predictor import predict_disease


# Image location
IMAGE_PATH = (
    Path(__file__).resolve().parent.parent
    / "test_images"
    / "leaf.jpg"
)


print("Loading image...")

image = Image.open(IMAGE_PATH)

result = predict_disease(image)


print("\n" + "=" * 50)
print("SMARTAGRI-AI ML PREDICTION")
print("=" * 50)

print("Disease:", result["disease"])
print(f"Confidence: {result['confidence']:.2f}%")
print(f"Inference latency: {result['latency_ms']:.2f} ms")
print("Class index:", result["class_index"])

print("=" * 50)