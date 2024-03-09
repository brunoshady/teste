from uuid import UUID

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.services.database import Base


class UserRoles(Base):
    __tablename__ = "user_roles"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    role = Column(String, nullable=False)
