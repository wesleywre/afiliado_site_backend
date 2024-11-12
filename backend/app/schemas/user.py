from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    name: str

    class Config:
        arbitrary_types_allowed = True

class UserCreate(UserBase):
    password: str

    class Config:
        arbitrary_types_allowed = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    name: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True