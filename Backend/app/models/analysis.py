from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SoilAnalysis(Base):
    __tablename__ = "soil_analysis"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    nitrogen = Column(Float, nullable=False)
    phosphorus = Column(Float, nullable=False)
    potassium = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    health_status = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="soil_analyses")

class DiseaseAnalysis(Base):
    __tablename__ = "disease_analysis"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    image_path = Column(String, nullable=False)
    crop = Column(String, nullable=False)
    disease = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="disease_analyses")

class IrrigationAnalysis(Base):
    __tablename__ = "irrigation_analysis"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    soil_moisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rain_probability = Column(Float, nullable=False)
    recommendation = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    best_time = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="irrigation_analyses")

class FarmActivity(Base):
    __tablename__ = "farm_activity"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    metric = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="analytics")