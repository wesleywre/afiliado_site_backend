from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from .comment import CommentOut
from .like import LikeOut
from .view import ViewOut

class CouponBase(BaseModel):
    title: str
    link: HttpUrl
    code: str

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[HttpUrl] = None
    code: Optional[str] = None
    approved: Optional[bool] = None

class CouponOut(CouponBase):
    id: int
    created_at: datetime
    approved: bool
    user_id: int
    comments: List[CommentOut] = []
    likes: List[LikeOut] = []
    views: List[ViewOut] = []

    class Config:
        orm_mode = True
