# app/src/schemas/comment.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    promotion_id: int


class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=1000)
    is_active: Optional[bool] = None


class Comment(CommentBase):
    id: int
    promotion_id: int
    user_id: int
    is_active: bool
    is_edited: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
