from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator


class UserRolesPatch(BaseModel):
    roles: List[str]


class UserRoles(BaseModel):
    id: UUID
    role: str

    # noinspection PyMethodParameters
    @field_validator('role')
    def validate_role(cls, role: str) -> str:
        return role.title()

    class Config:
        orm_mode = True
