import os
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta, UTC

import jwt

from ..domain.entities import TokenPairDTO, TokenPayloadDTO, TokenTypeEnum
from ..domain.exceptions import *

SECRET_KEY = os.getenv("AUTH_SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


class AuthService:
    def __init__(self, repo, users_client):
        self.repo = repo
        self.users = users_client

    def _hash_password(self, password: str) -> str:
        salt = SECRET_KEY[:16]
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._hash_password(plain_password) == hashed_password

    def _create_token(self, user_id: int, username: str, token_type: TokenTypeEnum) -> tuple[str, datetime, str]:
        jti = str(uuid.uuid4())

        if token_type == TokenTypeEnum.ACCESS:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        expire = datetime.now(UTC) + expires_delta

        payload = {
            "sub": str(user_id),
            "username": username,
            "type": token_type.value,
            "exp": expire,
            "jti": jti,
            "iat": datetime.now(UTC),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token, expire, jti

    def _decode_token(self, token: str) -> TokenPayloadDTO:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            return TokenPayloadDTO(
                user_id=int(payload["sub"]),
                username=payload["username"],
                token_type=TokenTypeEnum(payload["type"]),
                exp=datetime.fromtimestamp(payload["exp"], UTC),
                jti=payload["jti"],
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise TokenError(f"Invalid token: {str(e)}")

    def register(self, username: str, email: str, password: str) -> dict:
        """Регистрация: создаём user в users_service, credentials в auth"""
        username = username.strip().lower()
        email = email.strip().lower()

        if len(password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters")

        # Создаём пользователя в users_service
        user = self.users.create_user(username=username, email=email)

        # Сохраняем credentials
        hashed_password = self._hash_password(password)
        self.repo.save_credentials(user["id"], hashed_password)

        # Возвращаем с обоими флагами
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "rsl_status": user["rsl_status"],
            "is_verified": user.get("is_verified", False),
            "is_active": True,  # auth управляет этим флагом
            "created_at": user["created_at"],
        }

    def login(self, username: str, password: str) -> TokenPairDTO:
        # Получаем user из users_service для валидации
        user = self.users.get_by_username(username.strip().lower())
        if user is None:
            raise InvalidCredentialsError("Invalid credentials")

        if not user.get("is_active", True):
            raise UserInactiveError("User account is disabled")

        # Проверяем пароль локально
        creds = self.repo.get_credentials(user["id"])
        if creds is None or not self._verify_password(password, creds["password_hash"]):
            raise InvalidCredentialsError("Invalid credentials")

        access_token, access_exp, access_jti = self._create_token(
            user["id"], user["username"], TokenTypeEnum.ACCESS
        )
        refresh_token, refresh_exp, refresh_jti = self._create_token(
            user["id"], user["username"], TokenTypeEnum.REFRESH
        )

        self.repo.save_token(jti=access_jti, user_id=user["id"], token_type=TokenTypeEnum.ACCESS, expires_at=access_exp)
        self.repo.save_token(jti=refresh_jti, user_id=user["id"], token_type=TokenTypeEnum.REFRESH,
                             expires_at=refresh_exp)

        return TokenPairDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def verify_token(self, token: str) -> dict:
        """Валидация токена, возвращает user из users_service"""
        payload = self._decode_token(token)

        if payload.token_type != TokenTypeEnum.ACCESS:
            raise TokenError("Invalid token type")

        token_record = self.repo.get_token(payload.jti)
        if token_record and token_record.get("revoked"):
            raise TokenRevokedError("Token has been revoked")

        # Получаем актуальные данные user из users_service
        user = self.users.get_by_id(payload.user_id)
        if user is None:
            raise UserNotFoundError()

        return user

    def refresh_access_token(self, refresh_token: str) -> TokenPairDTO:
        payload = self._decode_token(refresh_token)

        if payload.token_type != TokenTypeEnum.REFRESH:
            raise TokenError("Invalid token type")

        token_record = self.repo.get_token(payload.jti)
        if token_record and token_record.get("revoked"):
            raise TokenRevokedError("Refresh token has been revoked")

        user = self.users.get_by_id(payload.user_id)
        if user is None:
            raise UserNotFoundError()

        self.repo.revoke_token(payload.jti)

        new_access_token, access_exp, access_jti = self._create_token(
            user["id"], user["username"], TokenTypeEnum.ACCESS
        )
        new_refresh_token, refresh_exp, refresh_jti = self._create_token(
            user["id"], user["username"], TokenTypeEnum.REFRESH
        )

        self.repo.save_token(jti=access_jti, user_id=user["id"], token_type=TokenTypeEnum.ACCESS, expires_at=access_exp)
        self.repo.save_token(jti=refresh_jti, user_id=user["id"], token_type=TokenTypeEnum.REFRESH,
                             expires_at=refresh_exp)

        return TokenPairDTO(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def revoke_token(self, token: str) -> None:
        try:
            payload = self._decode_token(token)
            self.repo.revoke_token(payload.jti)
        except TokenExpiredError:
            pass

    def change_password(self, user_id: int, old_password: str, new_password: str) -> None:
        if len(new_password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters")

        creds = self.repo.get_credentials(user_id)
        if creds is None:
            raise UserNotFoundError()

        if not self._verify_password(old_password, creds["password_hash"]):
            raise InvalidCredentialsError("Invalid current password")

        self.repo.update_password(user_id, self._hash_password(new_password))
        self.repo.revoke_all_user_tokens(user_id)