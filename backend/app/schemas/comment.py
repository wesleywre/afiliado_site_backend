from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

    class Config:
        orm_mode = True
