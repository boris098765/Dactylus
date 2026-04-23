from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()


class CredentialsORM(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # ← блокировка аккаунта
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))


class TokenORM(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    jti = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token_type = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))