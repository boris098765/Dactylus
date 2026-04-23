from fastapi import APIRouter, Depends, HTTPException, status

from ..domain.exceptions import *
from .deps import get_auth_service, get_current_user
from .schemas import (
    LoginRequest,
    TokenResponse,
    RegisterRequest,
    UserResponse,
    PasswordChangeRequest,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def handle_error(e: Exception):
    if isinstance(e, UserNotFoundError):
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    if isinstance(e, InvalidCredentialsError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))
    if isinstance(e, TokenError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))
    if isinstance(e, UserExistsError):
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    service=Depends(get_auth_service),
):
    try:
        user = service.register(
            username=data.username,
            email=data.email,
            password=data.password,
        )
        return user
    except Exception as e:
        handle_error(e)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    service=Depends(get_auth_service),
):
    try:
        tokens = service.login(
            username=data.username,
            password=data.password,
        )
        return tokens
    except Exception as e:
        handle_error(e)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    data: TokenResponse,
    service=Depends(get_auth_service),
):
    try:
        tokens = service.refresh_access_token(data.refresh_token)
        return tokens
    except Exception as e:
        handle_error(e)


@router.get("/me", response_model=UserResponse)
def get_me(user=Depends(get_current_user)):
    return user


@router.post("/logout")
def logout(
    data: TokenResponse,
    service=Depends(get_auth_service),
):
    try:
        service.revoke_token(data.access_token)
        return {"status": "ok"}
    except Exception as e:
        handle_error(e)


@router.post("/password/change")
def change_password(
    data: PasswordChangeRequest,
    user=Depends(get_current_user),
    service=Depends(get_auth_service),
):
    try:
        service.change_password(
            user_id=user.id,
            old_password=data.old_password,
            new_password=data.new_password,
        )
        return {"status": "ok"}
    except Exception as e:
        handle_error(e)