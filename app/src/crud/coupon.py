from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.coupon import Coupon, CouponStatus
from ..schemas.coupon import CouponCreate, CouponUpdate
from .base import CRUDBase


class CRUDCoupon(CRUDBase[Coupon, CouponCreate, CouponUpdate]):
    async def get_pending(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Coupon]:
        """Retorna todos os cupons pendentes de moderação"""
        return (
            db.query(self.model)
            .filter(self.model.status == CouponStatus.PENDING)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_active(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Coupon]:
        """Retorna cupons ativos e aprovados"""
        return (
            db.query(self.model)
            .filter(
                self.model.status == CouponStatus.APPROVED,
                self.model.is_active is True,
                (self.model.expires_at > func.now())
                | (self.model.expires_at.is_(None)),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def approve(
        self, db: Session, *, coupon_id: int, moderator_id: int
    ) -> Optional[Coupon]:
        """Aprova um cupom"""
        coupon = await self.get(db, id=coupon_id)
        if coupon:
            setattr(coupon, "status", CouponStatus.APPROVED)
            setattr(coupon, "moderator_id", moderator_id)
            setattr(coupon, "approved_at", func.now())
            db.add(coupon)
            await db.commit()
            await db.refresh(coupon)
        return coupon

    async def reject(
        self, db: Session, *, coupon_id: int, moderator_id: int, reason: str
    ) -> Optional[Coupon]:
        """Rejeita um cupom"""
        coupon = await self.get(db, id=coupon_id)
        if coupon:
            setattr(coupon, "status", CouponStatus.REJECTED)
            setattr(coupon, "moderator_id", moderator_id)
            setattr(coupon, "rejection_reason", reason)
            db.add(coupon)
            await db.commit()
            await db.refresh(coupon)
        return coupon

    async def increment_uses(self, db: Session, *, coupon_id: int) -> None:
        """Incrementa o contador de usos do cupom"""
        coupon = await self.get(db, id=coupon_id)
        if coupon:
            setattr(coupon, "times_used", coupon.times_used + 1)
            db.add(coupon)
            await db.commit()


CouponCRUD = CRUDCoupon(Coupon)
