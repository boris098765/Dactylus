from fastapi import APIRouter, Depends, HTTPException

from ...domain.exceptions import *
from ..deps import get_category_service
from ..schemas.category import (
    CategoryResponse,
    CategoryCreateRequest,
    CategoryUpdateRequest
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


def handle_error(e: Exception):
    if isinstance(e, CategoryNotFoundError):
        raise HTTPException(404, str(e))
    raise HTTPException(400, str(e))


@router.post("/", response_model=CategoryResponse)
def create_category(
    data: CategoryCreateRequest,
    service=Depends(get_category_service),
):
    try:
        category = service.create(
            name=data.name,
            parent_id=data.parent_id
        )
        return category
    except Exception as e:
        handle_error(e)


@router.get("/root", response_model=list[CategoryResponse])
def get_root_categories(service=Depends(get_category_service)):
    try:
        return service.get_root()
    except Exception as e:
        handle_error(e)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, service=Depends(get_category_service)):
    try:
        return service.get(category_id)
    except Exception as e:
        handle_error(e)


@router.get("/{category_id}/children", response_model=list[CategoryResponse])
def get_children(category_id: int, service=Depends(get_category_service)):
    try:
        return service.get_children(category_id)
    except Exception as e:
        handle_error(e)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdateRequest,
    service=Depends(get_category_service),
):
    try:
        return service.update(
            category_id,
            name=data.name,
            parent_id=data.parent_id
        )
    except Exception as e:
        handle_error(e)


@router.delete("/{category_id}")
def delete_category(category_id: int, service=Depends(get_category_service)):
    try:
        service.delete(category_id)
        return {"status": "ok"}
    except Exception as e:
        handle_error(e)
