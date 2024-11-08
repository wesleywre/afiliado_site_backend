from pydantic import BaseModel, constr

from .base import BaseSchema


class CommentBase(BaseModel):
    content: constr(min_length=1, max_length=1000)  # type: ignore


class CommentCreate(CommentBase):
    promotion_id: int


class CommentUpdate(CommentBase):
    pass


class Comment(BaseSchema, CommentBase):
    user_id: int
    promotion_id: int
