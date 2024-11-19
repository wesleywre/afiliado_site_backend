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


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    product: Optional[str] = None
    link: Optional[AnyUrl] = None
    price: Optional[float] = None
    comment: Optional[str] = None
    status: Optional[PromotionStatus] = None
    image: Optional[str] = None
    store: Optional[str] = None


class PromotionInDBBase(PromotionBase):
    id: int
    status: PromotionStatus
    user_id: int
    store: Optional[str] = ""
    image: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class Promotion(PromotionInDBBase):
    pass
