from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentInDBBase(CommentBase):
    id: int
    user_id: int

    model_config = {"from_attributes": True}


class Comment(CommentInDBBase):
    pass
