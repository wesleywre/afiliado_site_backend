# src/models/coupon.py

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from src.core.database import Base


class CouponStatus(PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, nullable=False)
    link = Column(String, nullable=False)
    code = Column(String, nullable=False)
    image = Column(String, nullable=True)
    comment = Column(Text, nullable=True)
    store = Column(String, nullable=True)
    status = Column(Enum(CouponStatus), default=CouponStatus.PENDING, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="coupons")
    comments = relationship("Comment", back_populates="coupon", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="coupon", cascade="all, delete-orphan")
