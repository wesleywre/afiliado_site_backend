from typing import List

from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

    class Config:
        arbitrary_types_allowed = True

class RoleCreate(RoleBase):
    pass

    class Config:
        arbitrary_types_allowed = True

class RoleUpdate(RoleBase):
    pass

    class Config:
        arbitrary_types_allowed = True

class RoleOut(RoleBase):
    id: int
    permissions: List[int] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True