from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    farm_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    soil_type = Column(String, nullable=False)
    crop_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="farms")
    soil_analyses = relationship("SoilAnalysis", back_populates="farm", cascade="all, delete-orphan")
    disease_analyses = relationship("DiseaseAnalysis", back_populates="farm", cascade="all, delete-orphan")
    irrigation_analyses = relationship("IrrigationAnalysis", back_populates="farm", cascade="all, delete-orphan")
    analytics = relationship("FarmActivity", back_populates="farm", cascade="all, delete-orphan")