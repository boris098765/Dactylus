from pydantic import BaseModel
from datetime import datetime

from ..domain.entities import RSLStatusEnum


class UserCreateRequest(BaseModel):
    username: str
    email: str
    rsl_status: RSLStatusEnum


class UserUpdateRequest(BaseModel):
    username: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    rsl_status: str
    is_verified: bool
    created_at: datetime