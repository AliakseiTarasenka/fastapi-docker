from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.domain.models.book_tags import Tag
from src.domain.models.books import Book
from src.presentation.web.schemas.book_tags import TagCreateModel, TagAddModel


class ITagRepository(ABC):
    """Interface for tag repository"""

    @abstractmethod
    async def get_tags(self) -> List[Tag]:
        """Get all tags"""
        raise NotImplementedError()

    @abstractmethod
    async def get_tag_by_uid(self, tag_uid: UUID) -> Optional[Tag]:
        """Get tag by uid"""
        raise NotImplementedError()

    @abstractmethod
    async def add_tag(self, tag_data: TagCreateModel) -> Optional[Tag]:
        """Create a tag"""
        raise NotImplementedError()

    @abstractmethod
    async def add_tags_to_book(self, book_uid: UUID, tag_data: TagAddModel) -> Book:
        """Add tags to a book"""
        raise NotImplementedError()

    @abstractmethod
    async def update_tag(self, tag_uid, tag_update_data: TagCreateModel) -> Optional[Tag]:
        """Update a tag"""
        raise NotImplementedError()

    @abstractmethod
    async def delete_tag(self, tag_uid: UUID) -> bool:
        """Delete a tag"""
        raise NotImplementedError()
