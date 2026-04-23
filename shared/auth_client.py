import os
import httpx
from functools import wraps
from fastapi import HTTPException, status, Request

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8002")


class AuthClient:
    def __init__(self, base_url: str = AUTH_SERVICE_URL):
        self.base_url = base_url.rstrip("/")

    async def verify_token(self, token: str) -> dict:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{self.base_url}/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid token")
            response.raise_for_status()
            return response.json()


def require_auth(func):
    """Декоратор для защиты эндпоинтов"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request')
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

        if not request:
            raise HTTPException(status_code=500, detail="Request object not found")

        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.replace("Bearer ", "")
        client = AuthClient()
        user = await client.verify_token(token)

        # Добавляем user в kwargs
        kwargs['current_user'] = user
        return await func(*args, **kwargs)

    return wrapper