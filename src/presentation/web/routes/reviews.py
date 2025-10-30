from typing import List

from fastapi import APIRouter, Depends, status

from src.application.services.reviews import ReviewService
from src.domain.models.users import User
from src.infrastructure.dependencies.authentication import get_current_user
from src.infrastructure.dependencies.authorization import get_role_checker
from src.infrastructure.dependencies.repositories import get_review_service
from src.presentation.web.schemas.reviews import (
    ReviewCreateModel,
    ReviewUpdateModel,
    ReviewModel,
    BookRatingStatsModel,
)

review_router = APIRouter()

# Role checkers
user_role_checker = Depends(get_role_checker(["admin", "user"]))
admin_role_checker = Depends(get_role_checker(["admin"]))


@review_router.get(
    "/reviews",
    response_model=List[ReviewModel],
    dependencies=[admin_role_checker],
    status_code=status.HTTP_200_OK,
)
async def get_all_reviews(
    limit: int = 100, offset: int = 0, review_service: ReviewService = Depends(get_review_service)
):
    """
    Get all reviews (Admin only)

    - **limit**: Maximum number of reviews to return (default: 100)
    - **offset**: Number of reviews to skip (default: 0)
    """
    reviews = await review_service.get_all_reviews(limit=limit, offset=offset)
    return reviews


@review_router.get(
    "/reviews/{review_uid}",
    response_model=ReviewModel,
    dependencies=[user_role_checker],
    status_code=status.HTTP_200_OK,
)
async def get_review(review_uid: str, review_service: ReviewService = Depends(get_review_service)):
    """
    Get a specific review by UID

    - **review_uid**: UUID of the review
    """
    review = await review_service.get_review(review_uid)
    return review


@review_router.get(
    "/reviews/book/{book_uid}", response_model=List[ReviewModel], status_code=status.HTTP_200_OK
)
async def get_book_reviews(
    book_uid: str,
    limit: int = 100,
    offset: int = 0,
    review_service: ReviewService = Depends(get_review_service),
):
    """
    Get all reviews for a specific book (Public)

    - **book_uid**: UUID of the book
    - **limit**: Maximum number of reviews to return (default: 100)
    - **offset**: Number of reviews to skip (default: 0)
    """
    reviews = await review_service.get_book_reviews(book_uid=book_uid, limit=limit, offset=offset)
    return reviews


@review_router.get(
    "/reviews/book/{book_uid}/stats",
    response_model=BookRatingStatsModel,
    status_code=status.HTTP_200_OK,
)
async def get_book_rating_stats(
    book_uid: str, review_service: ReviewService = Depends(get_review_service)
):
    """
    Get rating statistics for a book (Public)

    - **book_uid**: UUID of the book

    Returns total reviews count and average rating
    """
    stats = await review_service.get_book_rating_stats(book_uid)
    return stats


@review_router.get(
    "/reviews/user/me",
    response_model=List[ReviewModel],
    dependencies=[user_role_checker],
    status_code=status.HTTP_200_OK,
)
async def get_my_reviews(
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    """
    Get all reviews by the current user

    - **limit**: Maximum number of reviews to return (default: 100)
    - **offset**: Number of reviews to skip (default: 0)
    """
    reviews = await review_service.get_user_reviews(
        user_email=current_user.email, limit=limit, offset=offset
    )
    return reviews


@review_router.post(
    "/reviews/book/{book_uid}",
    response_model=ReviewModel,
    dependencies=[user_role_checker],
    status_code=status.HTTP_201_CREATED,
)
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    """
    Add a review to a book

    - **book_uid**: UUID of the book to review
    - **review_data**: Review content (rating and text)

    Users can only review a book once
    """
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email, book_uid=book_uid, review_data=review_data
    )
    return new_review


@review_router.patch(
    "/reviews/{review_uid}",
    response_model=ReviewModel,
    dependencies=[user_role_checker],
    status_code=status.HTTP_200_OK,
)
async def update_review(
    review_uid: str,
    review_data: ReviewUpdateModel,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    """
    Update a review

    - **review_uid**: UUID of the review to update
    - **review_data**: Updated review content (rating and/or text)

    Users can only update their own reviews
    """
    updated_review = await review_service.update_review(
        review_uid=review_uid, user_email=current_user.email, review_data=review_data
    )
    return updated_review


@review_router.delete(
    "/reviews/{review_uid}",
    dependencies=[user_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    review_uid: str,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
):
    """
    Delete a review

    - **review_uid**: UUID of the review to delete

    Users can only delete their own reviews
    """
    await review_service.delete_review(review_uid=review_uid, user_email=current_user.email)
    return None
