from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status  # Depends is a dependency injection system
from fastapi.exceptions import HTTPException

from src.infrastructure.db.database import get_session
from src.infrastructure.persistence.books_repository import BookRepository
from src.infrastructure.service.authentication import AccessTokenBearer
from src.infrastructure.service.authorization import RoleChecker
from src.presentation.web.schemas.books import (
    Book,
    BookCreateModel,
    BookUpdateModel,
)  # import schemas

# Global level functions/names
access_token_bearer = AccessTokenBearer()
app = APIRouter()
books_repository = BookRepository(Depends(get_session))
role_checker = Depends(RoleChecker(["admin", "user"]))


@app.get("/books", response_model=List[Book])
async def get_all_books(
    token_details=Depends(access_token_bearer),
) -> List[Book]:
    """Connect to the database and load books."""
    books = await books_repository.get_all_books()
    return books


@app.post(
    "/books", response_model=Book, status_code=status.HTTP_201_CREATED, dependencies=[role_checker]
)
async def create_a_book(
    book_data: BookCreateModel,
    token_details=Depends(access_token_bearer),
):
    """Connect to the database and create new book."""
    user_id = token_details.get("user")["user_uid"]
    new_book = await books_repository.create_book(book_data, user_id)
    if not new_book:
        raise HTTPException(status_code=500, detail="Failed to create book")

    return new_book


@app.get(
    "/books/{book_uid}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_book(
    book_uid: UUID,
    token_details=Depends(access_token_bearer),
) -> Book:
    """Connect to the database and load book by uid."""
    book = await books_repository.get_book(book_uid)
    if book:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch(
    "/books/{book_uid}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def update_book(
    book_uid: UUID,
    book_update_data: BookUpdateModel,
    token_details=Depends(access_token_bearer),
) -> Book:
    """Connect to the database and update book by uid."""
    updated_book = await books_repository.update_book(book_uid, book_update_data)
    if update_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return updated_book


@app.delete(
    "/books/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: UUID,
    token_details=Depends(access_token_bearer),
):
    deleted = await books_repository.delete_book(book_uid)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_uid} not found",
        )
    return {}
