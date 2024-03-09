from typing import List

from src.utils.exceptions import UserWithoutRolesException, InvalidUserRoleException

ADMIN_ROLE = 'admin'
MODIFIER_ROLE = 'modifier'
WATCHER_ROLE = 'watcher'
DEFAULT_ROLES = (ADMIN_ROLE, MODIFIER_ROLE, WATCHER_ROLE)


def validate_roles(roles: List):
    if not roles:
        raise UserWithoutRolesException()

    for role in roles:
        if role.lower() not in DEFAULT_ROLES:
            raise InvalidUserRoleException("Invalid user role!")


def validate_existing_roles(existing_roles: List, new_roles: List):
    validate_roles(new_roles)
    existing_roles = [role.role for role in existing_roles]

    # Admin can do anything
    if ADMIN_ROLE in existing_roles:
        return

    # Watcher cannot assume any other role
    if len(existing_roles) == 1 and existing_roles[0] == WATCHER_ROLE:
        if ADMIN_ROLE in new_roles or MODIFIER_ROLE in new_roles:
            raise InvalidUserRoleException("Watcher role cannot assign Admin or Modifier role!")

    # Modifier cannot assume Admin role
    elif MODIFIER_ROLE in existing_roles and ADMIN_ROLE in new_roles:
        raise InvalidUserRoleException("Modifier role cannot assign Admin role!")
