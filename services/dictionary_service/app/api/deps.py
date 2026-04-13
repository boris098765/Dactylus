from fastapi import Depends

from ..domain.services import CategoryService
from ..infra.db import SessionLocal
from ..infra.repositories import CategoryRepository


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_category_service(session = Depends(get_session)):
    repo = CategoryRepository(session)
    return CategoryService(repo)