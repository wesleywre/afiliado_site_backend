# src/schemas/user.py

from typing import List, Optional

from pydantic import BaseModel, EmailStr
from src.schemas.promotion import Promotion  # Importar o schema Promotion se necessário


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    is_active: bool = True
    role: str = "user"


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    role: str

    model_config = {"from_attributes": True}


class UserInDBBase(UserBase):
    id: int

    model_config = {"from_attributes": True}


class UserResponse(UserInDBBase):
    pass


class UserWithPromotions(UserInDBBase):
    promotions: List[Promotion] = []

    model_config = {"from_attributes": True}
