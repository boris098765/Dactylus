from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..domain.service import AuthService
from ..domain.exceptions import TokenError, UserNotFoundError
from ..infra.db import SessionLocal
from ..infra.repo import AuthRepository
from ..infra.clients import UsersClient

security = HTTPBearer(auto_error=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_users_client():
    return UsersClient()


def get_auth_service(
        session=Depends(get_session),
        users_client=Depends(get_users_client)
):
    repo = AuthRepository(session)
    return AuthService(repo, users_client)


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        service: AuthService = Depends(get_auth_service)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        user = service.verify_token(token)
        return user
    except TokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )