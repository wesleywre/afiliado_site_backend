from typing import List

from pydantic import BaseModel

from backend.app.models.permission import Permission


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    permissions: List["Permission"] = []

    class Config:
        orm_mode = True
