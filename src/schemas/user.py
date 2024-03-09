from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.schemas.user_roles import UserRoles


class UserCreate(BaseModel):
    name: str
    email: str
    roles: List[str]


class User(BaseModel):
    id: UUID
    name: str
    email: str

    roles: List[UserRoles]

    # noinspection PyMethodParameters
    @field_validator('name')
    def validate_role(cls, name: str) -> str:
        return name.title()

    class Config:
        orm_mode = True
