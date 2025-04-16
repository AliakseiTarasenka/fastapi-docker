from datetime import datetime, date, timezone
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.books import Book
from src.web.schemas.books import BookCreateModel
from fastapi import HTTPException
from fastapi.exceptions import ResponseValidationError

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

        except ResponseValidationError as val_error:
            print("Validation error:", val_error)
            return []
        except HTTPException as http_error:
            print("HTTP error:", http_error)
            return []
        except Exception as e:
            print("An error occurred:", e)
            return []
        else:
            return result.all()

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        """ Create a new book
        Args:
            book_data (BookCreateModel): data to create a new
        Returns:
            Book: the new book
        """
        try:
            book_data_dict = book_data.model_dump()
            new_book = Book(**book_data_dict)
            new_book.published_date = datetime.strptime(book_data_dict["published_date"], "%Y-%m-%d")
            session.add(new_book)
            """Commit the current transaction to ensure that the changes are persisted in the database."""
            await session.commit()
        except HTTPException as http_error:
            print("HTTP error:", http_error)
            return [] 
        except Exception as e:
            print("An error occurred:", e)
            return []
        else:
            return new_book

    async def get_book(self, book_id: str, session: AsyncSession):
        """ Get a book by id
            Returns:
                Book: the book
        """
        statement = select(Book).where(Book.uid == book_id)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def update_book(self, book_uid: str, update_data: BookCreateModel, session: AsyncSession):
        """ Update book by id
            book_id (str)
            update_data (BookCreateModel)
            Returns:
                Book: the book or None
        """
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                if key == "published_date":
                    value = datetime.strptime(value, "%Y-%m-%d")
                setattr(book_to_update, key, value)
            book_to_update.updated_at = datetime.now()

            await session.commit()

            return book_to_update
        else:
            return None


    async def delete_book(self, book_id: str, session: AsyncSession):
        try:
            book_to_delete = await self.get_book(book_id, session)
            if book_to_delete is not None:
                await session.delete(book_to_delete)
                await session.commit()
                return {}
            else:
                return None
        except HTTPException as http_error:
            print("HTTP error:", http_error)
            return None  # Or handle differently as per your application's needs
        except Exception as e:
            print("An error occurred:", e)
            return None