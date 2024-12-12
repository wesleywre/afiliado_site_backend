# src/models/coupon.py

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from src.core.database import Base


class CouponStatus(PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class Coupon(Base):
    __tablename__ = "coupons"

    __table_args__ = (
        # Índice para status e data de criação (ordenação)
        Index("idx_coupon_status_created_at", "status", "created_at"),
        # Índice para busca textual
        Index("idx_coupon_search_text", "product", "store", "comment"),
        # Índice para relacionamentos e filtros frequentes
        Index("idx_coupon_user_id", "user_id"),
        Index("idx_coupon_store", "store"),
        Index("idx_coupon_status", "status"),
    )

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
