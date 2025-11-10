from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.domain.repositories.tags_repository_interface import ITagRepository
from src.infrastructure.dependencies.authorization import get_role_checker
from src.infrastructure.dependencies.repositories import get_tags_repository
from src.presentation.web.schemas.book_tags import TagModel, TagCreateModel, TagAddModel
from src.presentation.web.schemas.books import Book

tags_router = APIRouter()
role_checker = Depends(get_role_checker(["admin", "user"]))


@tags_router.get("/tags", response_model=List[TagModel], dependencies=[role_checker])
async def get_all_tags(repo: ITagRepository = Depends(get_tags_repository)):
    tags = await repo.get_tags()

    return tags


@tags_router.post(
    "/tags",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def add_tag(
    tag_data: TagCreateModel, repo: ITagRepository = Depends(get_tags_repository)
) -> TagModel:
    tag_added = await repo.add_tag(tag_data=tag_data)

    return tag_added


@tags_router.post("/book/{book_uid}/tags", response_model=Book, dependencies=[role_checker])
async def add_tags_to_book(
    book_uid: UUID, tag_data: TagAddModel, repo: ITagRepository = Depends(get_tags_repository)
) -> Book:
    book_with_tag = await repo.add_tags_to_book(book_uid=book_uid, tag_data=tag_data)

    return book_with_tag


@tags_router.put("/tags/{tag_uid}", response_model=TagModel, dependencies=[role_checker])
async def update_tag(
    tag_uid: UUID,
    tag_update_data: TagCreateModel,
    repo: ITagRepository = Depends(get_tags_repository),
) -> TagModel:
    updated_tag = await repo.update_tag(tag_uid, tag_update_data)

    return updated_tag


@tags_router.delete(
    "/tags/{tag_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_tag(tag_uid: UUID, repo: ITagRepository = Depends(get_tags_repository)):
    updated_tag = await repo.delete_tag(tag_uid)

    return updated_tag
