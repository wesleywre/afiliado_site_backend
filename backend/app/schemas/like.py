from typing import Optional

from pydantic import BaseModel

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    user_id: int
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

class LikeUpdate(LikeBase):
    user_id: Optional[int] = None
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

class LikeOut(LikeBase):
    id: int
    user_id: int
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

    class Config:
        orm_mode = True