from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import (
    get_current_active_user,
    get_current_user,
    get_password_hash,
)
from src.models.user import User
from src.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserWithComments,
    UserWithCoupons,
    UserWithPromotions,
)

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        is_active=user_in.is_active,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/me/", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/users/me/", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_data = user_in.dict(exclude_unset=True)
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    for key, value in user_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """
    Usuário atual exclui sua própria conta.
    """
    db.delete(current_user)
    db.commit()
    return None


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Administrador ou moderador exclui a conta de um usuário.
    """
    if current_user.role not in ("ADMIN", "MODERATOR"):
        raise HTTPException(status_code=403, detail="Acesso negado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()
    return None


@router.get("/users/{user_id}/promotions/", response_model=UserWithPromotions)
def read_user_promotions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if user.id != current_user.id and current_user.role not in ("MODERATOR", "ADMIN"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


@router.get("/users/{user_id}/coupons/", response_model=UserWithCoupons)
def read_user_coupons(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if user.id != current_user.id and current_user.role not in ("MODERATOR", "ADMIN"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


@router.get("/users/{user_id}/comments/", response_model=UserWithComments)
def read_user_comments(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if user.id != current_user.id and current_user.role not in ("MODERATOR", "ADMIN"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user
