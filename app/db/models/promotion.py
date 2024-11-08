from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ...models.promotion import PromotionStatus
from ..base import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    price = Column(Float)
    original_price = Column(Float, nullable=True)
    link = Column(String)
    store = Column(String(100))
    image_url = Column(String, nullable=True)
    status = Column(Enum(PromotionStatus), default=PromotionStatus.pending)
    user_id = Column(Integer, ForeignKey("users.id"))
    moderator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    moderation_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="promotions", foreign_keys=[user_id])
    moderator = relationship("User", foreign_keys=[moderator_id])
    comments = relationship("Comment", back_populates="promotion")
