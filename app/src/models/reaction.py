# src/models/reaction.py

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from src.core.database import Base


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reactions")
    promotion = relationship("Promotion", back_populates="reactions")
    coupon = relationship("Coupon", back_populates="reactions")

    __table_args__ = (
        UniqueConstraint("user_id", "promotion_id", name="_user_promotion_uc"),
        UniqueConstraint("user_id", "coupon_id", name="_user_coupon_uc"),
    )
