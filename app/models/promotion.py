from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, confloat, constr

from .base import BaseSchema


class PromotionStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class PromotionBase(BaseModel):
    title: constr(min_length=3, max_length=200)  # type: ignore
    description: constr(min_length=10, max_length=2000)  # type: ignore
    price: confloat(gt=0)  # type: ignore
    original_price: Optional[confloat(gt=0)] = None  # type: ignore
    link: HttpUrl
    store: constr(min_length=2, max_length=100)  # type: ignore
    image_url: Optional[HttpUrl] = None


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(PromotionBase):
    status: Optional[PromotionStatus] = None
    moderation_notes: Optional[str] = None


class Promotion(BaseSchema, PromotionBase):
    status: PromotionStatus = PromotionStatus.pending
    user_id: int
    moderator_id: Optional[int] = None
    moderation_notes: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
