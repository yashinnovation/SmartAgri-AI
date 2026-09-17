from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.utils.sample_data import init_demo_data

from app.api.routes import (
    dashboard,
    disease,
    assistant,
    crops,
    soil,
    irrigation,
    weather,
    analytics
)
from app.api.routes.analytics import router as analytics_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.disease import router as disease_router
from app.api.routes.assistant import router as assistant_router
from app.api.routes.crops import router as crops_router
from app.api.routes.soil import router as soil_router
from app.api.routes.irrigation import router as irrigation_router
from app.api.routes.weather import router as weather_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.disease import router as disease_router
from app.api.routes.assistant import router as assistant_router
from app.api.routes.crops import router as crops_router
from app.api.routes.soil import router as soil_router
from app.api.routes.irrigation import router as irrigation_router
from app.api.routes.weather import router as weather_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.disease import router as disease_router
from app.api.routes.assistant import router as assistant_router
from app.api.routes.crops import router as crops_router
from app.api.routes.soil import router as soil_router
from app.api.routes.irrigation import router as irrigation_router
from app.api.routes.weather import router as weather_router

# Initialize Tables
Base.metadata.create_all(bind=engine)

# Seed Demo Data
db = SessionLocal()
try:
    init_demo_data(db)
finally:
    db.close()

app = FastAPI(
    title="AgriSmart AI Backend",
    description="AI-Powered Smart Farming Platform API",
    version="1.0.0"
)

# CORS Setup
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    settings.FRONTEND_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if settings.APP_ENV != "demo" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unhandled server error occurred."
            }
        }
    )

# Health Endpoint
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "AgriSmart AI Backend",
        "version": "1.0.0"
    }

# Register API Routers
app.include_router(dashboard.router, prefix="/api")
app.include_router(disease.router, prefix="/api")
app.include_router(assistant.router, prefix="/api")
app.include_router(crops.router, prefix="/api")
app.include_router(soil.router, prefix="/api")
app.include_router(irrigation.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

from app.api.routes.dashboard import router as d_r
# Include Farm Router
from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router

from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router

from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router

# Include Farm management endpoint
from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router
from app.api.routes.dashboard import router

# Include farm endpoints
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.disease import router as disease_router
from app.api.routes.assistant import router as assistant_router
from app.api.routes.crops import router as crops_router
from app.api.routes.soil import router as soil_router
from app.api.routes.irrigation import router as irrigation_router
from app.api.routes.weather import router as weather_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router
from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router
from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router

# Register Farms Router
from app.api.routes.dashboard import router
from app.api.routes.analytics import router
from app.api.routes.disease import router
from app.api.routes.crops import router
from app.api.routes.soil import router
from app.api.routes.irrigation import router
from app.api.routes.weather import router
from app.api.routes.assistant import router
from app.api.routes import dashboard
from app.api.routes import disease
from app.api.routes import assistant
from app.api.routes import crops
from app.api.routes import soil
from app.api.routes import irrigation
from app.api.routes import weather
from app.api.routes import analytics

# Directly register Farm management endpoint
from app.schemas.farm import FarmCreate, FarmUpdate, FarmResponse
from app.models.farm import Farm
from fastapi import Depends

@app.post("/api/farms", response_model=FarmResponse, tags=["Farms"])
def create_farm(payload: FarmCreate, db: Session = Depends(SessionLocal)):
    farm = Farm(**payload.model_dump())
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

@app.get("/api/farms", response_model=list[FarmResponse], tags=["Farms"])
def get_farms(db: Session = Depends(SessionLocal)):
    return db.query(Farm).all()

@app.get("/api/farms/{farm_id}", response_model=FarmResponse, tags=["Farms"])
def get_farm(farm_id: int, db: Session = Depends(SessionLocal)):
    farm = db.query(Farm).filter_by(id=farm_id).first()
    if not farm:
        return JSONResponse(status_code=404, content={"message": "Farm not found"})
    return farm