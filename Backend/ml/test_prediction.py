import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path
import time


# --------------------------------
# Paths
# --------------------------------
ML_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ML_DIR.parent

MODEL_PATH = ML_DIR / "plant_disease_efficientnet.keras"
CLASS_NAMES_PATH = ML_DIR / "class_names.txt"
IMAGE_PATH = BACKEND_DIR / "test_images" / "leaf.jpg"


# --------------------------------
# Load model
# --------------------------------
print("Loading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# --------------------------------
# Load class names
# --------------------------------
with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]

print(f"Number of classes: {len(class_names)}")


# --------------------------------
# Load image
# --------------------------------
print("Loading image...")

image = Image.open(IMAGE_PATH).convert("RGB")

print("Original image size:", image.size)


# --------------------------------
# Get model input size
# --------------------------------
input_height = model.input_shape[1]
input_width = model.input_shape[2]

image = image.resize((input_width, input_height))


# --------------------------------
# Convert image to array
# --------------------------------
image_array = np.array(image, dtype=np.float32)

# Add batch dimension
image_array = np.expand_dims(image_array, axis=0)


# --------------------------------
# Prediction
# --------------------------------
print("Running prediction...")

start_time = time.perf_counter()

predictions = model.predict(image_array, verbose=0)

end_time = time.perf_counter()

latency_ms = (end_time - start_time) * 1000


# --------------------------------
# Get prediction
# --------------------------------
predictions = predictions[0]

predicted_index = np.argmax(predictions)

confidence = float(predictions[predicted_index]) * 100

predicted_class = class_names[predicted_index]


# --------------------------------
# Display result
# --------------------------------
print("\n" + "=" * 50)
print("DISEASE DETECTION RESULT")
print("=" * 50)

print("Disease:", predicted_class)
print(f"Confidence: {confidence:.2f}%")
print(f"Inference latency: {latency_ms:.2f} ms")

print("=" * 50)