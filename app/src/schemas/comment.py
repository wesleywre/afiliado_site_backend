from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentInDBBase(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None

    model_config = {"from_attributes": True}


class Comment(CommentInDBBase):
    replies: List["Comment"] = []  # Lista de respostas

    model_config = {"from_attributes": True}


Comment.model_rebuild()
