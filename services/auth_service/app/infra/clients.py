import os
import httpx
from fastapi import HTTPException

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://users:8001")


class UsersClient:
    def __init__(self, base_url: str = USERS_SERVICE_URL):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=5.0)

    def create_user(self, username: str, email: str) -> dict:
        response = self.client.post(
            f"{self.base_url}/users/",
            json={"username": username, "email": email, "rsl_status": "learner"}
        )
        if response.status_code == 409:
            raise Exception("User already exists")
        response.raise_for_status()
        return response.json()

    def get_by_username(self, username: str) -> dict | None:
        # Используем поиск или прямой эндпоинт если есть
        response = self.client.get(f"{self.base_url}/users/by-username/{username}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_by_id(self, user_id: int) -> dict | None:
        response = self.client.get(f"{self.base_url}/users/{user_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


class UsersClientAsync:
    """Async версия для использования в зависимостях FastAPI"""

    def __init__(self, base_url: str = USERS_SERVICE_URL):
        self.base_url = base_url.rstrip("/")

    async def get_by_id(self, user_id: int) -> dict | None:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{self.base_url}/users/{user_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()