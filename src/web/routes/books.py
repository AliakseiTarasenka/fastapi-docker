from fastapi import status, APIRouter, Depends # Depends is a dependency injection system
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession # AsyncSession is used to handle database sessions asynchronously
from src.web.schemas.books import Book, BookCreateModel, BookUpdateModel # import schemas.
from src.persistence.database import get_session
from src.service.books import BookService

app = APIRouter()
book_service = BookService()

@app.get("/books", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    """Connect to the database and load books """
    books = await book_service.get_all_books(session)
    return books


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:

    updated_book = await book_service.update_book(book_id, book_update_data, session)
    if update_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return updated_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_id, session)

    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    else:
        return {}