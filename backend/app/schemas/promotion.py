from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from .comment import CommentOut
from .like import LikeOut
from .view import ViewOut

class PromotionBase(BaseModel):
    title: str
    link: HttpUrl
    price: float
    description: Optional[str] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[HttpUrl] = None
    price: Optional[float] = None
    description: Optional[str] = None
    approved: Optional[bool] = None

class PromotionOut(PromotionBase):
    id: int
    created_at: datetime
    approved: bool
    user_id: int
    comments: List[CommentOut] = []
    likes: List[LikeOut] = []
    views: List[ViewOut] = []

    class Config:
        orm_mode = True
