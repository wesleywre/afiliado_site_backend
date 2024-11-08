from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, constr

from .base import BaseSchema


class CouponBase(BaseModel):
    code: constr(min_length=1, max_length=50)  # type: ignore
    description: constr(min_length=10, max_length=1000)  # type: ignore
    store: constr(min_length=2, max_length=100)  # type: ignore
    link: HttpUrl
    expires_at: Optional[datetime] = None
    discount_value: Optional[float] = None
    discount_percentage: Optional[float] = None


class CouponCreate(CouponBase):
    pass


class CouponUpdate(CouponBase):
    pass


class Coupon(BaseSchema, CouponBase):
    user_id: int
    status: PromotionStatus = PromotionStatus.pending
    moderator_id: Optional[int] = None
