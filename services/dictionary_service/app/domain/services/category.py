from shared.utils.slug import generate_slug

from ..entities import CategoryDTO
from ..exceptions import *


class CategoryService:
    def __init__(self, repo):
        self.repo = repo

    def get(self,
            category_id: int
    ):
        category = self.repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        return self._to_dto(category)

    def get_root(self):
        categories = self.repo.get_root()
        return [self._to_dto(c) for c in categories]

    def get_children(self,
            category_id: int
    ):
        category = self.repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        return [self._to_dto(child) for child in self.repo.get_children(category_id)]

    def create(self,
            name: str,
            parent_id: int | None
    ):
        name = name.strip()
        if not name:
            raise CategoryValidationError("Name is required")
        if self.repo.get_by_name(name):
            raise CategoryNameExistsError()

        if parent_id is not None:
            parent = self.repo.get_by_id(parent_id)
            if parent is None:
                raise CategoryParentNotFoundError()

        slug = generate_slug(name)
        if self.repo.get_by_slug(slug):
            raise CategorySlugExistsError()

        category = self.repo.create({
            "name": name,
            "slug": slug,
            "parent_id": parent_id
        })
        return self._to_dto(category)

    def update(self,
            category_id: int,
            name: str | None = None,
            parent_id: int | None = None
    ):
        category = self.repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()

        if name is not None:
            name = name.strip()
            if not name:
                raise CategoryValidationError()

            existing_text = self.repo.get_by_name(name)
            if existing_text and existing_text.id != category_id:
                raise CategoryNameExistsError()
            category.name = name

            slug = generate_slug(name)
            existing_slug = self.repo.get_by_slug(slug)
            if existing_slug and existing_slug.id != category_id:
                raise CategorySlugExistsError()
            category.slug = slug

        if parent_id is not None:
            parent = self.repo.get_by_id(parent_id)
            if parent is None:
                raise CategoryParentNotFoundError()

            if parent_id == category_id:
                raise CategoryCircularReferenceError()

            category.parent_id = parent_id

        return self._to_dto(self.repo.save(category))

    def delete(self,
            category_id: int
    ):
        category = self.repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()

        children = self.repo.get_children(category_id)
        if children:
            raise CategoryHasChildrenError()

        self.repo.delete(category)
        return True

    def _to_dto(self, orm_category):
        """Преобразование ORM модели в DTO"""
        return CategoryDTO(
            id=orm_category.id,
            name=orm_category.name,
            slug=orm_category.slug,
            parent_id=orm_category.parent_id,
            order=orm_category.order,
            created_at=getattr(orm_category, 'created_at', None)
        )