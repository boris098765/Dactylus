from pydantic import BaseModel
from datetime import datetime


class CategoryCreateRequest(BaseModel):
    name: str
    parent_id: int | None = None


class CategoryUpdateRequest(BaseModel):
    name: str | None = None
    parent_id: int | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: int | None
    order: int | None
    created_at: datetime | None