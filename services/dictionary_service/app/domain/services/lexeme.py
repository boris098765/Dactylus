from shared.utils import generate_slug

from ..entities import (
    ModerationStatusEnum,
    TextLexemeDTO,
    GestureLexemeDTO
)
from ..exceptions import *


class BaseLexemeService:
    def __init__(self, repo):
        self.repo = repo

    def get(self,
            lexeme_id: int
    ):
        obj = self.repo.get_by_id(lexeme_id)
        if obj is None:
            raise LexemeNotFoundError()
        return self._to_dto(obj)

    def create(self,
            text: str,
            categories: list[int],
            author_id: int
    ):
        text = text.strip()
        if not text:
            raise LexemeValidationError("Text is required")

        slug = generate_slug(text)

        if self.repo.get_by_slug(slug):
            raise LexemeSlugExistsError()

        obj = self.repo.create({
            "text": text,
            "slug": slug,
            "categories": categories,
            "author_id": author_id,
            "moderation_status": ModerationStatusEnum.PENDING,
        })

        return self._to_dto(obj)

    def update(self,
            lexeme_id: int,
            **kwargs
    ):
        obj = self.repo.get_by_id(lexeme_id)
        if obj is None:
            raise LexemeNotFoundError()

        if "text" in kwargs:
            text = kwargs["text"].strip()
            if not text:
                raise LexemeValidationError()

            existing = self.repo.get_by_text(text)
            if existing and existing.id != lexeme_id:
                raise LexemeTextExistsError()
            obj.text = text

            slug = generate_slug(text)
            existing_slug = self.repo.get_by_slug(slug)
            if existing_slug and existing_slug.id != lexeme_id:
                raise LexemeSlugExistsError()
            obj.slug = slug

        return self._to_dto(self.repo.save(obj))

    def delete(self, lexeme_id: int):
        obj = self.repo.get_by_id(lexeme_id)
        if obj is None:
            raise LexemeNotFoundError()

        composes = self.repo.get_composes(lexeme_id)
        if composes:
            raise LexemeHasComposesError()

        self.repo.delete(obj)
        return True

    def _to_dto(self, orm_obj):
        raise NotImplementedError


class TextLexemeService(BaseLexemeService):
    def create(self,
            text: str,
            categories: list[int],
            author_id: int,
            is_letter: bool = False,
            letter_char: str | None = None
    ):
        dto = super().create(text, categories, author_id)

        obj = self.repo.get_by_id(dto.id)
        obj.is_letter = is_letter
        obj.letter_char = letter_char

        return self._to_dto(self.repo.save(obj))

    def _to_dto(self, obj):
        return TextLexemeDTO(
            id=obj.id,
            text=obj.text,
            slug=obj.slug,
            categories=obj.categories,
            meanings=obj.meanings,
            author_id=obj.author_id,
            moderation_status=obj.moderation_status,
            created_at=obj.created_at,
            is_letter=obj.is_letter,
            letter_char=obj.letter_char,
        )


class GestureLexemeService(BaseLexemeService):
    def create(self,
            text: str,
            categories: list[int],
            author_id: int,
            is_letter: bool = False,
            letter_char: str | None = None
    ):
        dto = super().create(text, categories, author_id)

        obj = self.repo.get_by_id(dto.id)
        obj.is_letter = is_letter
        obj.letter_char = letter_char

        return self._to_dto(self.repo.save(obj))

    def _to_dto(self, obj):
        return GestureLexemeDTO(
            id=obj.id,
            text=obj.text,
            slug=obj.slug,
            categories=obj.categories,
            meanings=obj.meanings,
            author_id=obj.author_id,
            moderation_status=obj.moderation_status,
            created_at=obj.created_at,
            is_letter=obj.is_letter,
            letter_char=obj.letter_char,
        )
