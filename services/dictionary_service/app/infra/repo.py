from typing import Optional
from .models import CategoryORM


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def save(self, obj: CategoryORM):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def create(self, data: dict):
        obj = CategoryORM(**data)
        return self.save(obj)

    def delete(self, obj: CategoryORM):
        self.session.delete(obj)
        self.session.commit()

    def get_by_id(self, category_id: int) -> Optional[CategoryORM]:
        return self.session.query(CategoryORM).filter_by(id=category_id).first()

    def get_by_name(self, name: str) -> Optional[CategoryORM]:
        return self.session.query(CategoryORM).filter_by(name=name).first()

    def get_by_slug(self, slug: str) -> Optional[CategoryORM]:
        return self.session.query(CategoryORM).filter_by(slug=slug).first()

    def exists_by_slug(self, slug: str) -> bool:
        return self.session.query(
            self.session.query(CategoryORM).filter_by(slug=slug).exists()
        ).scalar()

    def get_children(self, parent_id: int) -> list[CategoryORM]:
        return self.session.query(CategoryORM).filter_by(parent_id=parent_id).all()

    def get_root(self) -> list[CategoryORM]:
        return self.session.query(CategoryORM).filter(CategoryORM.parent_id.is_(None)).all()

    def search_by_name(self, query: str) -> list[CategoryORM]:
        return (
            self.session.query(CategoryORM)
            .filter(CategoryORM.name.ilike(f"%{query}%"))
            .all()
        )

    def search_by_prefix(self, query: str) -> list[CategoryORM]:
        return (
            self.session.query(CategoryORM)
            .filter(CategoryORM.name.ilike(f"{query}%"))
            .all()
        )
