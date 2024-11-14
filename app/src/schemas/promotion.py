# src/schemas/promotion.py

from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel


class PromotionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class PromotionBase(BaseModel):
    product: str
    link: AnyUrl
    price: float
    comment: Optional[str] = None


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    product: Optional[str]
    link: Optional[AnyUrl]
    price: Optional[float]
    comment: Optional[str]
    status: Optional[PromotionStatus]


class PromotionInDBBase(PromotionBase):
    id: int
    status: PromotionStatus
    user_id: int

    model_config = {"from_attributes": True}


class Promotion(PromotionInDBBase):
    pass
