from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, UTC

from ..domain.entities import ModerationStatusEnum

Base = declarative_base()


class CategoryORM(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    order = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))

    parent = relationship("CategoryORM", remote_side=[id], backref="children")

class TextLexemeORM(Base):
    __tablename__ = "text_lexemes"

    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    author_id = Column(Integer, nullable=False)

    moderation_status = Column(
        Enum(ModerationStatusEnum),
        nullable=False,
        default=ModerationStatusEnum.PENDING
    )
