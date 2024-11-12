from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str

    class Config:
        arbitrary_types_allowed = True

class PermissionCreate(PermissionBase):
    pass

    class Config:
        arbitrary_types_allowed = True

class PermissionUpdate(PermissionBase):
    pass

    class Config:
        arbitrary_types_allowed = True

class PermissionOut(PermissionBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True