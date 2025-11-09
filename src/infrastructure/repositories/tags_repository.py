from typing import Optional, List
from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.book_tags import Tag
from src.domain.models.books import Book
from src.domain.repositories.tags_repository_interface import ITagRepository
from src.infrastructure.repositories.books_repository import BookRepository
from src.presentation.web.schemas.book_tags import TagCreateModel, TagAddModel


class TagRepository(ITagRepository):
    """This class provides methods to create, read, update, and delete books."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tags(self) -> List[Tag]:
        """Get all tags"""

        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await self.session.exec(statement)

        return result.all()

    async def add_tags_to_book(self, book_uid: UUID, tag_data: TagAddModel) -> Book:
        """Add tags to a book"""
        book_repository = BookRepository(self.session)

        book = await book_repository.get_book(book_id=book_uid)

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        for tag_item in tag_data.tags:
            result = await self.session.exec(select(Tag).where(Tag.name == tag_item.name))

            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item.name)

            book.tags.append(tag)

        self.session.add(book)

        await self.session.commit()

        await self.session.refresh(book)

        return book

    async def get_tag_by_uid(self, tag_uid: UUID) -> Optional[Tag]:
        """Get tag by uid"""

        statement = select(Tag).where(Tag.uid == tag_uid)

        result = await self.session.exec(statement)

        return result.first()

    async def add_tag(self, tag_data: TagCreateModel) -> Optional[Tag]:
        """Create a tag"""

        statement = select(Tag).where(Tag.name == tag_data.name)

        result = await self.session.exec(statement)

        tag = result.first()

        if tag:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tag exists")

        new_tag = Tag(name=tag_data.name)

        self.session.add(new_tag)

        await self.session.commit()

        return new_tag

    async def update_tag(self, tag_uid: UUID, tag_update_data: TagCreateModel) -> Optional[Tag]:
        """Update a tag"""

        tag = await self.get_tag_by_uid(tag_uid)

        update_data_dict = tag_update_data.model_dump()

        for key, value in update_data_dict.items():
            setattr(tag, key, value)

            await self.session.commit()

            await self.session.refresh(tag)

        return tag

    async def delete_tag(self, tag_uid: UUID) -> bool:
        """Delete a tag"""

        tag = self.get_tag_by_uid(tag_uid)

        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag does not exist")

        await self.session.delete(tag)

        await self.session.commit()

        return True
