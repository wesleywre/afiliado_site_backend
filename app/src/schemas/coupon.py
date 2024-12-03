from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel


class CouponStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class CouponBase(BaseModel):
    product: str
    link: AnyUrl
    code: str
    comment: Optional[str] = None


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    product: Optional[str] = None
    link: Optional[AnyUrl] = None
    code: Optional[str] = None
    comment: Optional[str] = None
    status: Optional[CouponStatus] = None
    image: Optional[str] = None
    store: Optional[str] = None


class CouponInDBBase(CouponBase):
    id: int
    status: CouponStatus
    user_id: int
    store: Optional[str] = ""
    image: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class Coupon(CouponInDBBase):
    pass
