from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..models.promotion import Promotion, PromotionStatus
from ..schemas.promotion import PromotionCreate, PromotionUpdate
from .base import CRUDBase


class CRUDPromotion(CRUDBase[Promotion, PromotionCreate, PromotionUpdate]):
    async def get_active(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Promotion]:
        query = (
            select(self.model)
            .filter(
                self.model.status == PromotionStatus.APPROVED,
                self.model.is_active == True,  # noqa :E712
                (self.model.expires_at > func.now())
                | (self.model.expires_at.is_(None)),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_pending(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Promotion]:
        query = (
            select(self.model)
            .filter(self.model.status == PromotionStatus.PENDING)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def approve(
        self, db: Session, *, promotion_id: int, moderator_id: int
    ) -> Optional[Promotion]:
        """Aprova uma promoção"""
        promotion = await self.get(db, id=promotion_id)
        if promotion:
            setattr(promotion, "status", PromotionStatus.APPROVED)
            setattr(promotion, "moderator_id", moderator_id)
            setattr(promotion, "approved_at", func.now())
            db.add(promotion)
            await db.commit()
            await db.refresh(promotion)
        return promotion

    async def reject(
        self, db: Session, *, promotion_id: int, moderator_id: int, reason: str
    ) -> Optional[Promotion]:
        """Rejeita uma promoção"""
        promotion = await self.get(db, id=promotion_id)
        if promotion:
            setattr(promotion, "status", PromotionStatus.REJECTED)
            setattr(promotion, "moderator_id", moderator_id)
            setattr(promotion, "rejection_reason", reason)
            db.add(promotion)
            await db.commit()
            await db.refresh(promotion)
        return promotion

    async def increment_views(self, db: Session, *, promotion_id: int) -> None:
        """Incrementa o contador de visualizações"""
        promotion = await self.get(db, id=promotion_id)
        if promotion:
            setattr(promotion, "views_count", promotion.views_count + 1)
            db.add(promotion)
            await db.commit()

    async def increment_clicks(self, db: Session, *, promotion_id: int) -> None:
        """Incrementa o contador de cliques"""
        promotion = await self.get(db, id=promotion_id)
        if promotion:
            setattr(promotion, "clicks_count", promotion.clicks_count + 1)
            db.add(promotion)
            await db.commit()


PromotionCRUD = CRUDPromotion(Promotion)
