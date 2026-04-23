from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TokenTypeEnum(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


@dataclass
class TokenPayloadDTO:
    user_id: int
    username: str
    token_type: TokenTypeEnum
    exp: datetime
    jti: str


@dataclass
class TokenPairDTO:
    access_token: str
    refresh_token: str
    expires_in: int