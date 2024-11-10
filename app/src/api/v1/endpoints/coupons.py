from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_active_user, get_current_moderator
from ....crud.coupon import CouponCRUD
from ....models.user import User, UserRole
from ....schemas.coupon import Coupon, CouponCreate, CouponUpdate

router = APIRouter()


@router.post("/", response_model=Coupon)
async def create_coupon(
    *,
    coupon_in: CouponCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Coupon:
    """Criar um novo cupom"""
    return await CouponCRUD.create(db, obj_in=coupon_in, user_id=current_user.id)


@router.get("/", response_model=List[Coupon])
async def list_coupons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Coupon]:
    """Listar cupons ativos e aprovados"""
    return await CouponCRUD.get_active(db, skip=skip, limit=limit)


@router.get("/pending", response_model=List[Coupon])
async def list_pending_coupons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_moderator),
    db: Session = Depends(get_db),
) -> List[Coupon]:
    """Listar cupons pendentes (apenas moderadores)"""
    return await CouponCRUD.get_pending(db, skip=skip, limit=limit)


@router.get("/{coupon_id}", response_model=Coupon)
async def get_coupon(coupon_id: int, db: Session = Depends(get_db)) -> Coupon:
    """Obter um cupom específico"""
    coupon = await CouponCRUD.get(db, id=coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom não encontrado"
        )
    return coupon


@router.put("/{coupon_id}", response_model=Coupon)
async def update_coupon(
    coupon_id: int,
    coupon_in: CouponUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Coupon:
    """Atualizar um cupom existente"""
    coupon = await CouponCRUD.get(db, id=coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom não encontrado"
        )
    if coupon.user_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar este cupom",
        )
    return await CouponCRUD.update(db, db_obj=coupon, obj_in=coupon_in)


@router.put("/{coupon_id}/approve")
async def approve_coupon(
    coupon_id: int,
    current_user: User = Depends(get_current_moderator),
    db: Session = Depends(get_db),
) -> Coupon:
    """Aprovar um cupom (apenas moderadores)"""
    coupon = await CouponCRUD.approve(
        db, coupon_id=coupon_id, moderator_id=current_user.id
    )
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom não encontrado"
        )
    return coupon


@router.put("/{coupon_id}/reject")
async def reject_coupon(
    coupon_id: int,
    reason: str,
    current_user: User = Depends(get_current_moderator),
    db: Session = Depends(get_db),
) -> Coupon:
    """Rejeitar um cupom (apenas moderadores)"""
    coupon = await CouponCRUD.reject(
        db, coupon_id=coupon_id, moderator_id=current_user.id, reason=reason
    )
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom não encontrado"
        )
    return coupon


@router.post("/{coupon_id}/use")
async def register_use(coupon_id: int, db: Session = Depends(get_db)):
    """Registrar uso de um cupom"""
    await CouponCRUD.increment_uses(db, coupon_id=coupon_id)
    return {"status": "success"}
