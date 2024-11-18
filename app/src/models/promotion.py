# src/models/promotion.py

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from src.core.database import Base


class PromotionStatus(PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, nullable=False)
    link = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=True)
    comment = Column(Text, nullable=True)
    store = Column(String, nullable=True)
    status = Column(Enum(PromotionStatus), default=PromotionStatus.PENDING, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="promotions")
    comments = relationship("Comment", back_populates="promotion", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="promotion", cascade="all, delete-orphan")
