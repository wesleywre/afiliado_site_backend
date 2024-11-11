from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class View(Base):
    __tablename__ = "views"
    
    id = Column(Integer, primary_key=True, index=True)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    view_count = Column(Integer, default=0)
    
    # Relacionamentos
    promotion = relationship("Promotion", back_populates="views")
    coupon = relationship("Coupon", back_populates="views")
