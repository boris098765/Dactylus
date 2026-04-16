from .entities import UserDTO
from .exceptions import *


class UserService:
    def __init__(self, repo):
        self.repo = repo

    def get(self,
            user_id: int
    ):
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return self._to_dto(user)

    def create(self,
            username: str,
            email: str,
            rsl_status: str
    ):
        username = username.strip()
        if not username:
            raise UserValidationError("Userame is required")
        if self.repo.get_by_username(username):
            raise UserUsernameExistsError()

        email = email.strip()
        if not email:
            raise UserValidationError("Email is required")
        if self.repo.get_by_email(email):
            raise UserEmailExistsError()

        user = self.repo.create({
            "username": username,
            "email": email,
            "rsl_status": rsl_status
        })
        return self._to_dto(user)

    def update(self,
            user_id: int,
            username: str | None = None,
            email: str | None = None
    ):
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        if username is not None:
            username = username.strip()
            if not username:
                raise UserNotFoundError()

            existing = self.repo.get_by_username(username)
            if existing and existing.id != user_id:
                raise UserUsernameExistsError()
            user.username = username

        if email is not None:
            email = email.strip()
            if not email:
                raise UserValidationError()

            existing = self.repo.get_by_email(email)
            if existing and existing.id != user_id:
                raise UserEmailExistsError()
            user.email = email

        return self._to_dto(self.repo.save(user))

    def delete(self,
            user_id: int
    ):
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        self.repo.delete(user)
        return True

    def _to_dto(self, orm_user):
        return UserDTO(
            id=orm_user.id,
            username=orm_user.username,
            email=orm_user.email,
            is_verified=orm_user.is_verified,
            rsl_status=orm_user.rsl_status,
            created_at=getattr(orm_user, 'created_at', None)
        )