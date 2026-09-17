# Crop ideal profiles for recommendation calculation
CROP_RULES = {
    "Rice": {
        "ph": (5.5, 7.0),
        "temp": (20, 35),
        "rain": (100, 300),
        "soils": ["Loamy", "Clay"],
        "n": (80, 120), "p": (40, 60), "k": (40, 60)
    },
    "Maize": {
        "ph": (5.8, 7.2),
        "temp": (18, 30),
        "rain": (50, 100),
        "soils": ["Loamy", "Sandy Loam"],
        "n": (60, 100), "p": (30, 50), "k": (30, 50)
    },
    "Cotton": {
        "ph": (6.0, 8.0),
        "temp": (21, 32),
        "rain": (50, 110),
        "soils": ["Black", "Loamy"],
        "n": (50, 90), "p": (20, 40), "k": (20, 40)
    },
    "Wheat": {
        "ph": (6.0, 7.5),
        "temp": (12, 25),
        "rain": (40, 90),
        "soils": ["Loamy", "Clay Loam"],
        "n": (70, 110), "p": (30, 50), "k": (30, 50)
    },
    "Tomato": {
        "ph": (6.0, 6.8),
        "temp": (18, 29),
        "rain": (40, 80),
        "soils": ["Loamy", "Sandy Loam"],
        "n": (70, 100), "p": (40, 60), "k": (50, 80)
    }
}

DISEASE_KNOWLEDGE_BASE = {
    "Tomato": [
        {
            "disease": "Tomato Early Blight",
            "confidence": 0.92,
            "severity": "Moderate",
            "recommendation": "Remove lower infected leaves, apply copper-based fungicide, and refrain from overhead irrigation."
        },
        {
            "disease": "Tomato Late Blight",
            "confidence": 0.88,
            "severity": "High",
            "recommendation": "Apply systemic fungicide immediately and improve field drainage to prevent spore dispersion."
        },
        {
            "disease": "Healthy",
            "confidence": 0.96,
            "severity": "None",
            "recommendation": "Maintain regular watering schedule and continue standard crop monitoring."
        }
    ],
    "Default": [
        {
            "disease": "Leaf Spot Disease",
            "confidence": 0.85,
            "severity": "Moderate",
            "recommendation": "Apply appropriate organic fungicide and ensure proper sunlight coverage."
        }
    ]
}