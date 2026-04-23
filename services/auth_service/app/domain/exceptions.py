class AuthError(Exception):
    pass


class UserNotFoundError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class TokenError(AuthError):
    pass


class TokenExpiredError(TokenError):
    pass


class TokenRevokedError(TokenError):
    pass


class UserExistsError(AuthError):
    pass


class UserInactiveError(AuthError):
    pass


class WeakPasswordError(AuthError):
    pass