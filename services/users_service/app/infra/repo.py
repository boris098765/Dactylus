from typing import Optional
from .models import UserORM


class UserRepository:
    def __init__(self, session):
        self.session = session

    def save(self, obj: UserORM):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def create(self, data: dict):
        obj = UserORM(**data)
        return self.save(obj)

    def delete(self, obj: UserORM):
        self.session.delete(obj)
        self.session.commit()

    def get_by_id(self, user_id: int) -> Optional[UserORM]:
        return self.session.query(UserORM).filter_by(id=user_id).first()

    def get_by_username(self, username: str) -> Optional[UserORM]:
        return self.session.query(UserORM).filter_by(username=username).first()

    def get_by_email(self, email: str) -> Optional[UserORM]:
        return self.session.query(UserORM).filter_by(email=email).first()