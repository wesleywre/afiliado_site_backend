from typing import Optional

from pydantic import BaseModel, EmailStr, constr

from .base import BaseSchema


class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)  # type: ignore
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: constr(min_length=8)  # type: ignore


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(BaseSchema, UserBase):
    pass


class UserInDB(User):
    hashed_password: str
