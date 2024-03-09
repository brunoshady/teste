from typing import List
from uuid import UUID

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.user_roles import UserRoles
from src.services.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)

    roles: Mapped[List["UserRoles"]] = relationship()
