# app/src/models/promotion.py
import enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class PromotionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PromotionCategory(str, enum.Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    HOME = "home"
    BOOKS = "books"
    GAMES = "games"
    FOOD = "food"
    OTHER = "other"


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    link = Column(String, nullable=False)

    # Preços
    original_price = Column(Float)
    price = Column(Float, nullable=False)
    discount_percentage = Column(Float)

    # Categorização
    category = Column(SQLEnum(PromotionCategory), default=PromotionCategory.OTHER)
    store = Column(String, nullable=False)

    # Relacionamentos com foreign keys explícitas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id], back_populates="promotions")

    moderator_id = Column(Integer, ForeignKey("users.id"))
    moderator = relationship(
        "User", foreign_keys=[moderator_id], back_populates="moderated_promotions"
    )

    # Status e controle
    status = Column(
        SQLEnum(PromotionStatus), default=PromotionStatus.PENDING, nullable=False
    )
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)

    # Métricas
    views_count = Column(Integer, default=0)
    clicks_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)

    # Timestamps
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))

    # Campos de moderação
    rejection_reason = Column(Text)
    moderation_notes = Column(Text)

    # Relacionamentos inversos
    likes = relationship(
        "PromotionLike", back_populates="promotion", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="promotion", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Promotion {self.title} ({self.status})>"
