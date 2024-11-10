from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_active_user, get_current_moderator
from ....crud.comment import CommentCRUD
from ....models.user import User
from ....schemas.comment import Comment, CommentCreate, CommentUpdate

router = APIRouter()


@router.post("/promotions/{promotion_id}/comments", response_model=Comment)
async def create_comment(
    promotion_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Comment:
    """Criar novo comentário em uma promoção"""
    return await CommentCRUD.create(
        db,
        obj_in=CommentCreate(text=comment_in.text, promotion_id=promotion_id),
        user_id=current_user.id,
    )


@router.get("/promotions/{promotion_id}/comments", response_model=List[Comment])
async def list_comments(
    promotion_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Comment]:
    """Listar comentários de uma promoção"""
    return await CommentCRUD.get_by_promotion(
        db, promotion_id=promotion_id, skip=skip, limit=limit
    )


@router.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Comment:
    """Atualizar um comentário"""
    comment = await CommentCRUD.get(db, id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado"
        )

    # Verifica se o usuário é o dono do comentário ou moderador
    if comment.user_id != current_user.id and current_user.role != "moderator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar este comentário",
        )

    return await CommentCRUD.update(db, db_obj=comment, obj_in=comment_in)


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Deletar um comentário"""
    comment = await CommentCRUD.get(db, id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado"
        )

    # Verifica se o usuário é o dono do comentário ou moderador
    if comment.user_id != current_user.id and current_user.role != "moderator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar este comentário",
        )

    await CommentCRUD.delete(db, id=comment_id)
    return {"message": "Comentário deletado com sucesso"}


@router.put("/comments/{comment_id}/moderate", response_model=Comment)
async def moderate_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_moderator),  # Usando get_current_moderator
    db: Session = Depends(get_db),
) -> Comment:
    """
    Moderação de comentário (apenas moderadores)
    Permite que moderadores editem ou desativem comentários
    """
    comment = await CommentCRUD.get(db, id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado"
        )

    return await CommentCRUD.update(db, db_obj=comment, obj_in=comment_in)
