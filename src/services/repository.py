import uuid
from uuid import UUID

from sqlalchemy import true
from sqlalchemy.orm import Session

from src.models.user import User
from src.models.user_roles import UserRoles
from src.schemas.user import UserCreate as UserCreateSchema
from src.schemas.user_roles import UserRolesPatch as UserRolesPatchSchema
from src.utils.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.utils.rules import validate_roles, validate_existing_roles


def get_user(db: Session, user_id: UUID):
    user = db.query(User).filter(User.is_active == true()).filter(User.id == user_id).first()

    if not user:
        raise UserNotFoundException()

    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(User).filter(User.is_active == true()).order_by(User.name).offset(skip).limit(limit).all()
    return users


def create_user(db: Session, user: UserCreateSchema):
    existing_user = db.query(User).filter(User.is_active == true()).filter(User.email == user.email).first()

    # Here we only validate email because we can have two persons with the same name
    if existing_user:
        raise UserAlreadyExistsException()

    validate_roles(user.roles)

    new_user = User(id=uuid.uuid4(), name=user.name.lower(), email=user.email.lower())

    for role in user.roles:
        user_role = UserRoles(id=uuid.uuid4(), role=role.lower())
        new_user.roles.append(user_role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def update_user_roles(db: Session, user_id: UUID, new_user_rules: UserRolesPatchSchema):
    user = db.query(User).filter(User.is_active == true()).filter(User.id == user_id).first()

    if not user:
        raise UserNotFoundException()

    # Validate roles rules
    validate_existing_roles(user.roles, new_user_rules.roles)

    user_roles = db.query(UserRoles).filter(UserRoles.user == user.id).all()
    [db.delete(role) for role in user_roles]

    for role in set(new_user_rules.roles):
        user_role = UserRoles(id=uuid.uuid4(), role=role.lower())
        user.roles.append(user_role)

    db.add(user)
    db.commit()
    db.refresh(user)


def delete_user(db, user_id):
    user = db.query(User).filter(User.is_active == true()).filter(User.id == user_id).first()

    if not user:
        raise UserNotFoundException()

    # Here we just mark the user as active = False to maintain records
    user.is_active = False

    db.add(user)
    db.commit()
    db.refresh(user)
