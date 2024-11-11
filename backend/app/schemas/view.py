from pydantic import BaseModel
from typing import Optional

class ViewBase(BaseModel):
    view_count: int = 1

class ViewCreate(ViewBase):
    pass

class ViewOut(ViewBase):
    id: int
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

    class Config:
        orm_mode = True
