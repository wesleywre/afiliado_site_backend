from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    link = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    approved = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="promotions")
    comments = relationship("Comment", back_populates="promotion")
    likes = relationship("Like", back_populates="promotion")
    views = relationship("View", back_populates="promotion")
