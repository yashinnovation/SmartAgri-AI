import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path
import time


# --------------------------------
# Paths
# --------------------------------
ML_DIR = Path(__file__).resolve().parent

MODEL_PATH = ML_DIR / "plant_disease_efficientnet.keras"
CLASS_NAMES_PATH = ML_DIR / "class_names.txt"


# --------------------------------
# Load model ONCE
# --------------------------------
print("Loading Plant Disease ML model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Plant Disease ML model loaded successfully.")


# --------------------------------
# Load class names
# --------------------------------
with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]


print(f"Loaded {len(class_names)} disease classes.")


# --------------------------------
# Prediction function
# --------------------------------
def predict_disease(image: Image.Image):

    # Convert to RGB
    image = image.convert("RGB")

    # Get model input size
    input_height = model.input_shape[1]
    input_width = model.input_shape[2]

    # Resize
    image = image.resize((input_width, input_height))

    # Convert to NumPy array
    image_array = np.array(image, dtype=np.float32)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # --------------------------------
    # Run inference
    # --------------------------------
    start_time = time.perf_counter()

    predictions = model.predict(
        image_array,
        verbose=0
    )

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    # --------------------------------
    # Get prediction
    # --------------------------------
    predictions = predictions[0]

    predicted_index = int(np.argmax(predictions))

    confidence = float(predictions[predicted_index])

    predicted_class = class_names[predicted_index]

    # --------------------------------
    # Return result
    # --------------------------------
    return {
        "class_index": predicted_index,
        "disease": predicted_class,
        "confidence": confidence * 100,
        "latency_ms": latency_ms
    }