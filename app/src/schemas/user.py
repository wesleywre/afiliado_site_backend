from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
from ..models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50) # type: ignore
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=8) # type: ignore

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=50)] = None # type: ignore
    full_name: Optional[str] = None
    password: Optional[constr(min_length=8)] = None # type: ignore

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None