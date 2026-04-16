from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

from ..domain.entities import RSLStatusEnum

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

    rsl_status = Column(
        Enum(RSLStatusEnum),
        nullable=False,
        default=RSLStatusEnum.LEARNER
    )