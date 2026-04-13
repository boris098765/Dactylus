from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class ModerationStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class CategoryDTO:
    id: int
    name: str
    slug: str
    parent_id: Optional[int]
    order: Optional[int]
    created_at: datetime

@dataclass
class LexemeDTO:
    id: int
    text: str
    slug: str
    categories: List[int]
    meanings: List[int]

    author_id: int
    moderation_status: ModerationStatusEnum
    created_at: datetime

@dataclass
class TextLexemeDTO(LexemeDTO):
    is_letter: bool
    letter_char: Optional[str]

@dataclass
class GestureLexemeDTO(LexemeDTO):
    is_letter: bool
    letter_char: Optional[str]

@dataclass
class TextLexemeComposeDTO(LexemeDTO):
    pass

@dataclass
class GestureLexemeComposeDTO(LexemeDTO):
    pass

@dataclass
class TextLexemeComposeItemDTO:
    id: int
    text_lexeme_id: int
    order: int

@dataclass
class GestureLexemeComposeItemDTO:
    id: int
    gesture_lexeme_id: int
    order: int

@dataclass
class LexemePairDTO:
    id: int
    text_lexeme: int
    gesture_lexeme: int

    author_id: int
    moderation_status: ModerationStatusEnum
    created_at: datetime