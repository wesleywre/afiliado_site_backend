from pydantic import BaseModel
from typing import Optional

class ViewBase(BaseModel):
    view_count: int

class ViewCreate(ViewBase):
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

class ViewUpdate(ViewBase):
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

class ViewOut(ViewBase):
    id: int
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

    class Config:
        orm_mode = True