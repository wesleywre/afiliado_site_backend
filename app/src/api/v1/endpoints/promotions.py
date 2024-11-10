# app/src/api/v1/endpoints/promotions.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_active_user, get_current_moderator
from ....crud.promotion import PromotionCRUD
from ....models.user import User, UserRole
from ....schemas.promotion import Promotion, PromotionCreate, PromotionUpdate

router = APIRouter()


@router.post("/", response_model=Promotion)
async def create_promotion(
    *,
    promotion_in: PromotionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Promotion:
    """Criar uma nova promoção"""
    return await PromotionCRUD.create(db, obj_in=promotion_in, user_id=current_user.id)


@router.get("/", response_model=List[Promotion])
async def list_promotions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Promotion]:
    """Listar promoções ativas e aprovadas"""
    return await PromotionCRUD.get_active(db, skip=skip, limit=limit)


@router.get("/pending", response_model=List[Promotion])
async def list_pending_promotions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_moderator),
    db: Session = Depends(get_db),
) -> List[Promotion]:
    """Listar promoções pendentes (apenas moderadores)"""
    return await PromotionCRUD.get_pending(db, skip=skip, limit=limit)


@router.get("/{promotion_id}", response_model=Promotion)
async def get_promotion(promotion_id: int, db: Session = Depends(get_db)) -> Promotion:
    """Obter uma promoção específica"""
    promotion = await PromotionCRUD.get(db, id=promotion_id)
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promoção não encontrada"
        )
    await PromotionCRUD.increment_views(db, promotion_id=promotion_id)
    return promotion


@router.put("/{promotion_id}/approve")
async def approve_promotion(
    promotion_id: int,
    current_user: User = Depends(get_current_moderator),
    db: Session = Depends(get_db),
) -> Promotion:
    """Aprovar uma promoção (apenas moderadores)"""
    promotion = await PromotionCRUD.approve(
        db, promotion_id=promotion_id, moderator_id=current_user.id
    )
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promoção não encontrada"
        )
    return promotion


@router.put("/{promotion_id}/reject")
async def reject_promotion(
    promotion_id: int,
    reason: str,
    current_user: User = Depends(get_current_moderator),
    db: Session = Depends(get_db),
) -> Promotion:
    """Rejeitar uma promoção (apenas moderadores)"""
    promotion = await PromotionCRUD.reject(
        db, promotion_id=promotion_id, moderator_id=current_user.id, reason=reason
    )
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promoção não encontrada"
        )
    return promotion


# Endpoint de atualização
@router.put("/{promotion_id}", response_model=Promotion)
async def update_promotion(
    promotion_id: int,
    promotion_in: PromotionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Promotion:
    """
    Atualizar promoção:
    - Usuários podem editar suas próprias promoções
    - Moderadores podem editar qualquer promoção
    """
    promotion = await PromotionCRUD.get(db, id=promotion_id)
    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Promoção não encontrada"
        )

    # Verifica permissões
    if promotion.user_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar esta promoção",
        )

    return await PromotionCRUD.update(db, db_obj=promotion, obj_in=promotion_in)


@router.post("/{promotion_id}/click")
async def register_click(promotion_id: int, db: Session = Depends(get_db)):
    """Registrar clique em uma promoção"""
    await PromotionCRUD.increment_clicks(db, promotion_id=promotion_id)
    return {"status": "success"}
