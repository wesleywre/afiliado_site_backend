# app/src/models/user.py
import enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    promotions = relationship(
        "Promotion", back_populates="user", foreign_keys="[Promotion.user_id]"
    )
    comments = relationship("Comment", back_populates="user")
    likes = relationship("PromotionLike", back_populates="user")

    # Relacionamentos de moderação
    moderated_promotions = relationship(
        "Promotion", back_populates="moderator", foreign_keys="[Promotion.moderator_id]"
    )
    coupons = relationship(
        "Coupon", back_populates="user", foreign_keys="[Coupon.user_id]"
    )
    moderated_coupons = relationship(
        "Coupon", back_populates="moderator", foreign_keys="[Coupon.moderator_id]"
    )

    def __repr__(self):
        return f"<User {self.email}>"
