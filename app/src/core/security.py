from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.core.config import settings
from src.core.database import get_db
from src.models.refresh_token import RefreshToken
from src.models.user import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    return _create_token(data, expires_delta, settings.SECRET_KEY)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    return _create_token(data, expires_delta, settings.REFRESH_SECRET_KEY)


def _create_token(data: dict, expires_delta: Optional[timedelta], secret_key: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def save_refresh_token(db: Session, refresh_token: str, user_id: int, expires: datetime):
    db_token = RefreshToken(token=refresh_token, user_id=user_id, expires_at=expires)
    db.add(db_token)
    db.commit()


def revoke_refresh_token(db: Session, refresh_token: str, user_id: int):
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token, RefreshToken.user_id == user_id)
        .first()
    )
    if db_token:
        db.delete(db_token)
        db.commit()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user
