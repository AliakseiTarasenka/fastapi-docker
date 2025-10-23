from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.models.books import Book
from src.presentation.web.schemas.books import BookCreateModel, BookUpdateModel


class IBookRepository(ABC):
    """Interface for book repository"""

    @abstractmethod
    async def get_all_books(self) -> List[Book]:
        pass

    @abstractmethod
    async def get_user_books(self, user_uid: UUID) -> List[Book]:
        pass

    @abstractmethod
    async def create_book(self, book_data: BookCreateModel, user_uid: UUID) -> Optional[Book]:
        pass

    @abstractmethod
    async def get_book(self, book_id: UUID) -> Optional[Book]:
        pass

    @abstractmethod
    async def update_book(self, book_uid: UUID, update_data: BookUpdateModel) -> Optional[Book]:
        pass

    @abstractmethod
    async def delete_book(self, book_id: UUID) -> bool:
        pass
