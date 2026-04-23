from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    rsl_status: str
    is_verified: bool      # ← подтверждён ли email
    is_active: bool = True # ← активен ли аккаунт (может быть отключён админом)
    created_at: datetime


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)