import pytest

from src.models.user_roles import UserRoles
from src.utils.exceptions import UserWithoutRolesException, InvalidUserRoleException
from src.utils.rules import validate_roles, validate_existing_roles, WATCHER_ROLE, ADMIN_ROLE, MODIFIER_ROLE


def test_validate_roles_empty():
    # arrange
    roles = []

    # act
    with pytest.raises(Exception) as excinfo:
        validate_roles(roles)

    # assert
    assert type(excinfo.value) is UserWithoutRolesException


def test_validate_roles_invalid_role():
    # arrange
    roles = ['undefined']

    # act
    with pytest.raises(Exception) as excinfo:
        validate_roles(roles)

    # assert
    assert type(excinfo.value) is InvalidUserRoleException


def test_validate_roles_watcher_to_modifier():
    # arrange
    existing_roles = [UserRoles(role=WATCHER_ROLE)]
    new_roles = [MODIFIER_ROLE]

    # act
    with pytest.raises(Exception) as excinfo:
        validate_existing_roles(existing_roles, new_roles)

    # assert
    assert type(excinfo.value) is InvalidUserRoleException


def test_validate_roles_watcher_to_admin():
    # arrange
    existing_roles = [UserRoles(role=WATCHER_ROLE)]
    new_roles = [ADMIN_ROLE]

    # act
    with pytest.raises(Exception) as excinfo:
        validate_existing_roles(existing_roles, new_roles)

    # assert
    assert type(excinfo.value) is InvalidUserRoleException


def test_validate_roles_modifier_to_admin():
    # arrange
    existing_roles = [UserRoles(role=MODIFIER_ROLE)]
    new_roles = [ADMIN_ROLE]

    # act
    with pytest.raises(Exception) as excinfo:
        validate_existing_roles(existing_roles, new_roles)

    # assert
    assert type(excinfo.value) is InvalidUserRoleException


def test_validate_roles_admin_to_modifier():
    # arrange
    existing_roles = [UserRoles(role=ADMIN_ROLE)]
    new_roles = [MODIFIER_ROLE]
    exception = None

    # act
    try:
        validate_existing_roles(existing_roles, new_roles)
    except Exception as e:
        exception = e

    # assert
    assert exception is None


def test_validate_roles_admin_to_watcher():
    # arrange
    existing_roles = [UserRoles(role=ADMIN_ROLE)]
    new_roles = [WATCHER_ROLE]
    exception = None

    # act
    try:
        validate_existing_roles(existing_roles, new_roles)
    except Exception as e:
        exception = e

    # assert
    assert exception is None


def test_validate_roles_modifier_to_watcher():
    # arrange
    existing_roles = [UserRoles(role=MODIFIER_ROLE)]
    new_roles = [WATCHER_ROLE]
    exception = None

    # act
    try:
        validate_existing_roles(existing_roles, new_roles)
    except Exception as e:
        exception = e

    # assert
    assert exception is None
