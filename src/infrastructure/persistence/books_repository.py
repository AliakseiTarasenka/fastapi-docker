from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from fastapi.exceptions import ResponseValidationError
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.books import Book
from src.domain.repositories.book_repository_interface import IBookRepository
from src.presentation.web.schemas.books import BookCreateModel, BookUpdateModel


class BookRepository(IBookRepository):
    """This class provides methods to create, read, update, and delete books."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self) -> List[Book]:
        """Get a list of all books
        Returns:
            list: list of books
        """
        statement = select(Book).order_by(desc(Book.created_at))
        try:
            result = await self.session.exec(statement)

        except ResponseValidationError as val_error:
            print(f"Validation error: {val_error}")
            return []
        except HTTPException as http_error:
            print(f"HTTP error: {http_error}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

        return result.all()

    async def get_user_books(self, user_uid: UUID) -> List[Book]:
        """Get a list of books for a user
        Args:
            user_uid (str): link user to book
        Returns:
            list: list of user books
        """
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))

        result = await self.session.exec(statement)

        return result.all()

    async def create_book(self, book_data: BookCreateModel, user_uid: UUID) -> Optional[Book]:
        """Create a new book
        Args:
            book_data (BookCreateModel): data to create a new Book
            user_uid (str): link user to book
        Returns:
            Book: the new book
        """
        try:
            book_data_dict = book_data.model_dump()
            new_book = Book(**book_data_dict)
            new_book.published_date = datetime.strptime(
                book_data_dict["published_date"], "%Y-%m-%d"
            )
            new_book.user_uid = user_uid

            self.session.add(new_book)
            """Commit the current transaction to ensure that the changes are
            persisted in the database."""
            await self.session.commit()

        except HTTPException as http_error:
            print("HTTP error:", http_error)
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None

        return new_book

    async def get_book(self, book_id: UUID) -> Optional[Book]:
        """Get a book by id
        Args:
            book_id (UUID): data to create a new Book
        Returns:
            Book: the book
        """
        statement = select(Book).where(Book.uid == book_id)
        result = await self.session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def update_book(self, book_uid: UUID, update_data: BookUpdateModel) -> Optional[Book]:
        """Update book by id
         Args:
            book_uid (UUID)
            update_data (BookUpdateModel)
        Returns:
            Book: the book or None
        """
        book_to_update = await self.get_book(book_uid)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                if key == "published_date":
                    value = datetime.strptime(value, "%Y-%m-%d")
                setattr(book_to_update, key, value)
            book_to_update.updated_at = datetime.now()

            await self.session.commit()

            return book_to_update

        return None

    async def delete_book(self, book_id: UUID) -> bool:
        """Delete book by id
        Args:
            book_id (UUID)
        Returns:
            bool: Turn True on success, False otherwise
        """
        try:
            book_to_delete = await self.get_book(book_id)
            if book_to_delete is not None:
                await self.session.delete(book_to_delete)
                await self.session.commit()
                return True

            return False
        except HTTPException as http_error:
            print("HTTP error:", http_error)
            return False  # Or handle differently as per your application's needs
        except Exception as e:
            print("An error occurred:", e)
            return False
