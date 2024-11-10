# app/src/schemas/coupon.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, validator

from ..models.coupon import CouponStatus


class CouponBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=2000)
    link: HttpUrl
    store: str = Field(..., min_length=2, max_length=100)
    discount_value: str = Field(..., min_length=1, max_length=50)
    min_purchase: Optional[str] = Field(None, max_length=50)
    expires_at: Optional[datetime] = None

    @validator("code")
    def code_must_be_uppercase(cls, v):
        return v.upper()


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=2000)
    link: Optional[HttpUrl] = None
    store: Optional[str] = Field(None, min_length=2, max_length=100)
    discount_value: Optional[str] = Field(None, min_length=1, max_length=50)
    min_purchase: Optional[str] = Field(None, max_length=50)
    expires_at: Optional[datetime] = None
    status: Optional[CouponStatus] = None
    rejection_reason: Optional[str] = None


class Coupon(CouponBase):
    id: int
    user_id: int
    moderator_id: Optional[int]
    status: CouponStatus
    is_active: bool
    times_used: int
    created_at: datetime
    updated_at: Optional[datetime]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]

    class Config:
        from_attributes = True
