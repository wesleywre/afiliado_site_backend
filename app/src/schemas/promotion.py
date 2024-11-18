# src/schemas/promotion.py

from datetime import datetime
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
    image: Optional[str] = None


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    product: Optional[str]
    link: Optional[AnyUrl]
    price: Optional[float]
    comment: Optional[str]
    status: Optional[PromotionStatus]
    image: Optional[str]
    store: Optional[str]


class PromotionInDBBase(PromotionBase):
    id: int
    status: PromotionStatus
    user_id: int
    store: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Promotion(PromotionInDBBase):
    pass
