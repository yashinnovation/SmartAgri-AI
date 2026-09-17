import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_crop_recommendation():
    payload = {
        "soil_type": "Loamy",
        "ph": 6.8,
        "nitrogen": 78,
        "phosphorus": 42,
        "potassium": 65,
        "temperature": 29,
        "humidity": 68,
        "rainfall": 120
    }
    response = client.post("/api/crops/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0

def test_soil_analysis():
    payload = {
        "farm_id": 1,
        "nitrogen": 78,
        "phosphorus": 42,
        "potassium": 65,
        "ph": 6.8
    }
    response = client.post("/api/soil/analyze", json=payload)
    assert response.status_code == 200
    assert "health_status" in response.json()

def test_irrigation_recommendation():
    payload = {
        "farm_id": 1,
        "crop": "Tomato",
        "soil_moisture": 38,
        "temperature": 31,
        "humidity": 55,
        "rain_probability": 20
    }
    response = client.post("/api/irrigation/recommend", json=payload)
    assert response.status_code == 200
    assert "status" in response.json()

def test_dashboard_endpoint():
    response = client.get("/api/dashboard/1")
    assert response.status_code == 200
    assert "summary" in response.json()