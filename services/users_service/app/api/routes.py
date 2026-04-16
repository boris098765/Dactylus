from fastapi import APIRouter, Depends, HTTPException

from ..domain.exceptions import *
from .deps import get_user_service
from .schemas import (
    UserResponse,
    UserCreateRequest,
    UserUpdateRequest
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def handle_error(e: Exception):
    if isinstance(e, UserNotFoundError):
        raise HTTPException(404, str(e))
    raise HTTPException(400, str(e))


@router.post("/", response_model=UserResponse)
def create_user(
        data: UserCreateRequest,
        service=Depends(get_user_service),
):
    try:
        user = service.create(
            username=data.username,
            email=data.email,
            rsl_status=data.rsl_status
        )
        return user
    except Exception as e:
        handle_error(e)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service=Depends(get_user_service)):
    try:
        return service.get(user_id)
    except Exception as e:
        handle_error(e)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        data: UserUpdateRequest,
        service=Depends(get_user_service),
):
    try:
        return service.update(
            user_id,
            username=data.username,
            email=data.email
        )
    except Exception as e:
        handle_error(e)


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        service=Depends(get_user_service)
):
    try:
        service.delete(user_id)
        return {"status": "ok"}
    except Exception as e:
        handle_error(e)
