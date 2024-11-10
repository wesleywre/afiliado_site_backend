# app/src/models/coupon.py
import enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class CouponStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False, index=True)
    description = Column(Text)
    link = Column(String, nullable=False)
    store = Column(String, nullable=False)
    discount_value = Column(String)
    min_purchase = Column(String)

    # Relacionamentos com chaves estrangeiras explícitas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id], back_populates="coupons")

    moderator_id = Column(Integer, ForeignKey("users.id"))
    moderator = relationship(
        "User", foreign_keys=[moderator_id], back_populates="moderated_coupons"
    )

    status = Column(SQLEnum(CouponStatus), default=CouponStatus.PENDING, nullable=False)

    is_active = Column(Boolean, default=True)
    times_used = Column(Integer, default=0)

    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))

    rejection_reason = Column(Text)

    def __repr__(self):
        return f"<Coupon {self.code} ({self.status})>"
