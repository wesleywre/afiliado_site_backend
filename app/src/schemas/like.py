# app/src/schemas/like.py
from datetime import datetime

from pydantic import BaseModel


class PromotionLikeBase(BaseModel):
    promotion_id: int
    user_id: int


class PromotionLikeCreate(PromotionLikeBase):
    pass


class PromotionLike(PromotionLikeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
