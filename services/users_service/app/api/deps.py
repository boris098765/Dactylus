from fastapi import Depends

from ..domain.service import UserService
from ..infra.db import SessionLocal
from ..infra.repo import UserRepository


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_user_service(session = Depends(get_session)):
    repo = UserRepository(session)
    return UserService(repo)