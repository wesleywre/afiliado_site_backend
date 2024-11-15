# src/schemas/reaction.py

from typing import Optional

from pydantic import BaseModel


class ReactionBase(BaseModel):
    promotion_id: Optional[int] = None
    coupon_id: Optional[int] = None


class ReactionCreate(ReactionBase):
    pass


class ReactionInDBBase(ReactionBase):
    id: int
    user_id: int

    model_config = {"from_attributes": True}


class Reaction(ReactionInDBBase):
    pass
