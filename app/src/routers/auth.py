from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.database import get_db
from src.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    get_password_hash,
    revoke_refresh_token,
    save_refresh_token,
)
from src.models.refresh_token import RefreshToken
from src.models.user import User as UserModel
from src.schemas.user import User, UserUpdate

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    expires_at = datetime.utcnow() + refresh_token_expires
    save_refresh_token(db, refresh_token, user.id, expires_at)

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=int(refresh_token_expires.total_seconds()),
        samesite="lax",
        secure=True,
    )
    return response


@router.post("/refresh-token")
def refresh_access_token(
    db: Session = Depends(get_db), refresh_token: Optional[str] = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token não encontrado.")
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Verificar se o refresh token está armazenado no banco de dados
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token, RefreshToken.user_id == user.id)
        .first()
    )
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou revogado.")
    # Verificar se o refresh token expirou
    if db_token.expires_at < datetime.now(timezone.utc):
        # Remover token expirado do banco
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expirado.")

    # Gerar novo access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    refresh_token: Optional[str] = Cookie(None),
):
    """
    Logout do usuário atual.
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token não encontrado.")

    # Revogar o refresh token
    revoke_refresh_token(db, refresh_token, current_user.id)

    # Deletar o cookie do refresh token no cliente
    response.delete_cookie(key="refresh_token")

    return None  # Retorna HTTP 204 No Content


@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """
    Obter informações do usuário atual.
    """
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    """
    Atualizar informações do usuário atual.
    """
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = get_password_hash(update_data.pop("password"))
        current_user.hashed_password = hashed_password
    for field, value in update_data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user
