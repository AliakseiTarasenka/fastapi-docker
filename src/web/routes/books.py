from typing import List
from fastapi import (APIRouter, Depends, status) # Depends is a dependency injection system
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession # AsyncSession is used to handle database sessions asynchronously

from src.db.database import get_session
from src.persistence.books_repository import BookRepository
from src.service.authentication import AccessTokenBearer
from src.web.schemas.books import (Book, BookCreateModel, BookUpdateModel) # import schemas

# Global level functions/names
access_token_bearer = AccessTokenBearer()
app = APIRouter()
books_repository = BookRepository()


@app.get("/books", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> List[Book]:
    """Connect to the database and load books."""
    books = await books_repository.get_all_books(session)
    return books


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    """Connect to the database and create new book."""
    new_book = await books_repository.create_book(book_data, session)
    return new_book


@app.get("/books/{book_uid}", response_model=Book)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> Book:
    """Connect to the database and load book by uid."""
    book = await books_repository.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@app.patch("/books/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> Book:
    """Connect to the database and update book by uid."""
    updated_book = await books_repository.update_book(book_uid, book_update_data, session)
    if update_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return updated_book


@app.delete("/books/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    book_to_delete = await books_repository.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_uid} not found",
        )
    else:
        return {}
