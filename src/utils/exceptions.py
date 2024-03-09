

class UserAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("There is already a user with this email address!")


class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__("User not found!")


class UserWithoutRolesException(Exception):
    def __init__(self):
        super().__init__("User must be created with roles!")


class InvalidUserRoleException(Exception):
    def __init__(self, *args, **kwargs):
        pass


def is_business_logic_exception(e):
    if isinstance(e, (UserAlreadyExistsException, UserWithoutRolesException, InvalidUserRoleException)):
        return True

    return False
