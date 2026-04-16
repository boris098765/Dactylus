class UserError(Exception):
    pass

class UserValidationError(UserError):
    pass

class UserNotFoundError(UserError):
    pass

class UserUsernameExistsError(UserError):
    pass

class UserEmailExistsError(UserError):
    pass