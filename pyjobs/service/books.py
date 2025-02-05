from datetime import datetime
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from pyjobs.models.books import Book
from pyjobs.web.schemas.books import BookCreateModel

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

class BookService:
    """
    This class provides methods to create, read, update, and delete books
    """
    async def get_all_books(self, session: AsyncSession):
        """ Get a list of all books
            Returns:
                list: list of books
        """
        statement = select(Book).order_by(desc(Book.created_at))

        try:
            result = await session.exec(statement)
            return result.all()
        except RequestValidationError as val_error:
            print("Validation error:", val_error)
            return []  # Or handle differently as per your application's needs
        except HTTPException as http_error:
            print("HTTP error:", http_error)
            return []  # Or handle differently as per your application's needs
        except Exception as e:
            print("An error occurred:", e)
            return []

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        """ Create a new book
        Args:
            book_data (BookCreateModel): data to create a new
        Returns:
            Book: the new book
        """
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")
        session.add(new_book)
        """Commit the current transaction to ensure that the changes are persisted in the database."""
        await session.commit()

        return new_book

    async def get_book(self, book_id: str, session: AsyncSession):
        """ Get a book by id
            Returns:
                Book: the book
        """
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def update_book(self, book_id: str, update_data: BookCreateModel, session: AsyncSession):
        """ Update book by id
            book_id (str)
            update_data (BookCreateModel)
            Returns:
                Book: the book or None
        """
        book_to_update = await self.get_book(book_id,session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                setattr(book_to_update,key, value)

            await session.commit()

            return book_to_update
        else:
            return None


    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_id,session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

            return {}
        else:
            return None