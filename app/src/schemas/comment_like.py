from pydantic import BaseModel


class CommentLikeBase(BaseModel):
    pass


class CommentLikeCreate(CommentLikeBase):
    comment_id: int


class CommentLike(CommentLikeBase):
    id: int
    user_id: int
    comment_id: int

    model_config = {"from_attributes": True}
