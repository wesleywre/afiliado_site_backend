from typing import Optional

from pydantic import BaseModel


class LikeBase(BaseModel):
    pass


class LikeCreate(LikeBase):
    pass


class LikeOut(LikeBase):
    id: int
    user_id: int
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

    class Config:
        orm_mode = True
