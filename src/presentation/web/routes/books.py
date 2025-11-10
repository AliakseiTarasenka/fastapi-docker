from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status  # Depends is a dependency injection system
from fastapi.exceptions import HTTPException

from src.application.errors import BookNotFound
from src.domain.repositories.book_repository_interface import IBookRepository
from src.infrastructure.dependencies.authorization import get_role_checker
from src.infrastructure.dependencies.repositories import get_book_repository
from src.infrastructure.service.auth.token_bearer import AccessTokenBearer
from src.presentation.web.schemas.books import (
    Book,
    BookDetailModel,
    BookCreateModel,
    BookUpdateModel,
)  # import schemas

# Global level functions/names
app = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(get_role_checker(["admin", "user"]))


@app.get("/books", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    token_details=Depends(access_token_bearer),
    repo: IBookRepository = Depends(get_book_repository),
) -> List[Book]:
    """Connect to the database and load books."""
    books = await repo.get_all_books()
    return books


@app.post(
    "/books", response_model=Book, status_code=status.HTTP_201_CREATED, dependencies=[role_checker]
)
async def create_a_book(
    book_data: BookCreateModel,
    token_details=Depends(access_token_bearer),
    repo: IBookRepository = Depends(get_book_repository),
):
    """Connect to the database and create new book."""
    user_id = token_details.get("user")["user_uid"]
    new_book = await repo.create_book(book_data, user_id)
    if not new_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create book"
        )

    return new_book


@app.get(
    "/books/{book_uid}",
    response_model=BookDetailModel,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_book(
    book_uid: UUID,
    token_details=Depends(access_token_bearer),
    repo: IBookRepository = Depends(get_book_repository),
) -> Book:
    """Connect to the database and load book by uid."""
    book = await repo.get_book(book_uid)
    if book:
        return book

    raise BookNotFound()


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
    repo: IBookRepository = Depends(get_book_repository),
) -> Book:
    """Connect to the database and update book by uid."""
    updated_book = await repo.update_book(book_uid, book_update_data)
    if update_book is None:
        raise BookNotFound()

    return updated_book


@app.delete(
    "/books/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: UUID,
    token_details=Depends(access_token_bearer),
    repo: IBookRepository = Depends(get_book_repository),
):
    deleted = await repo.delete_book(book_uid)

    if not deleted:
        raise BookNotFound()
    return {}
