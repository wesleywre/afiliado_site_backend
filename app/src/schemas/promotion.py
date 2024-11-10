# app/src/schemas/promotion.py
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, validator

from ..models.promotion import PromotionCategory, PromotionStatus


class CommentBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user_id: int
    promotion_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PromotionBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    link: HttpUrl
    original_price: Optional[Decimal] = Field(None, ge=0)
    price: Decimal = Field(..., ge=0)
    store: str = Field(..., min_length=2, max_length=100)
    category: PromotionCategory = Field(default=PromotionCategory.OTHER)
    expires_at: Optional[datetime] = None

    @validator("price")
    def price_must_be_less_than_original(cls, v, values):
        if "original_price" in values and values["original_price"] is not None:
            if v >= values["original_price"]:
                raise ValueError("Price must be less than original price")
        return v


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    link: Optional[HttpUrl] = None
    original_price: Optional[Decimal] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)
    store: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[PromotionCategory] = None
    expires_at: Optional[datetime] = None
    status: Optional[PromotionStatus] = None
    rejection_reason: Optional[str] = None
    moderation_notes: Optional[str] = None


class Promotion(PromotionBase):
    id: int
    user_id: int
    moderator_id: Optional[int]
    status: PromotionStatus
    is_active: bool
    is_featured: bool
    views_count: int
    clicks_count: int
    likes_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    moderation_notes: Optional[str]
    comments: List[Comment] = []

    class Config:
        from_attributes = True
