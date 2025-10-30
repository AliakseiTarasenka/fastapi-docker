import logging
from typing import List
from uuid import UUID

from src.domain.repositories.book_repository_interface import IBookRepository
from src.domain.repositories.reviews_repository_interface import IReviewRepository
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infrastructure.service.errors import (
    BookNotFound,
    UserNotFound,
    ReviewNotFound,
    ReviewAlreadyExists,
    UnauthorizedReviewAccess,
)
from src.presentation.web.schemas.reviews import (
    ReviewCreateModel,
    ReviewUpdateModel,
    ReviewModel,
    BookRatingStatsModel,
)

logger = logging.getLogger(__name__)


class ReviewService:
    """Service layer for review operations"""

    def __init__(
        self,
        review_repository: IReviewRepository,
        user_repository: IUserRepository,
        book_repository: IBookRepository,
    ):
        self.review_repository = review_repository
        self.user_repository = user_repository
        self.book_repository = book_repository

    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
    ) -> ReviewModel:
        """
        Add a review to a book

        Args:
            user_email: Email of the user creating the review
            book_uid: UID of the book being reviewed
            review_data: Review data (rating and text)

        Returns:
            ReviewModel: Created review

        Raises:
            BookNotFound: If book does not exist
            UserNotFound: If user does not exist
            ReviewAlreadyExists: If user has already reviewed this book
        """
        # Validate book exists
        book = await self.book_repository.get_book(UUID(book_uid))
        if not book:
            raise BookNotFound()

        # Validate user exists
        user = await self.user_repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFound()

        # Check if user already reviewed this book
        has_reviewed = await self.review_repository.user_has_reviewed_book(
            user_uid=user.uid, book_uid=UUID(book_uid)
        )
        if has_reviewed:
            raise ReviewAlreadyExists()

        # Create the review
        new_review = await self.review_repository.create_review(
            review_data=review_data, user_uid=user.uid, book_uid=UUID(book_uid)
        )

        logger.info(f"User {user_email} created review {new_review.uid} for book {book_uid}")
        return ReviewModel.model_validate(new_review)

    async def get_review(self, review_uid: str) -> ReviewModel:
        """
        Get a review by UID

        Args:
            review_uid: UID of the review

        Returns:
            ReviewModel: The requested review

        Raises:
            ReviewNotFound: If review does not exist
        """
        review = await self.review_repository.get_review_by_uid(UUID(review_uid))

        if not review:
            raise ReviewNotFound()

        return ReviewModel.model_validate(review)

    async def get_all_reviews(self, limit: int = 100, offset: int = 0) -> List[ReviewModel]:
        """
        Get all reviews with pagination

        Args:
            limit: Maximum number of reviews to return
            offset: Number of reviews to skip

        Returns:
            List[ReviewModel]: List of reviews
        """
        reviews = await self.review_repository.get_all_reviews(limit=limit, offset=offset)
        return [ReviewModel.model_validate(review) for review in reviews]

    async def get_book_reviews(
        self, book_uid: str, limit: int = 100, offset: int = 0
    ) -> List[ReviewModel]:
        """
        Get all reviews for a specific book

        Args:
            book_uid: UID of the book
            limit: Maximum number of reviews to return
            offset: Number of reviews to skip

        Returns:
            List[ReviewModel]: List of reviews for the book

        Raises:
            BookNotFound: If book does not exist
        """
        # Validate book exists
        book = await self.book_repository.get_book(UUID(book_uid))
        if not book:
            raise BookNotFound()

        reviews = await self.review_repository.get_reviews_by_book(
            book_uid=UUID(book_uid), limit=limit, offset=offset
        )

        return [ReviewModel.model_validate(review) for review in reviews]

    async def get_user_reviews(
        self, user_email: str, limit: int = 100, offset: int = 0
    ) -> List[ReviewModel]:
        """
        Get all reviews by a specific user

        Args:
            user_email: Email of the user
            limit: Maximum number of reviews to return
            offset: Number of reviews to skip

        Returns:
            List[ReviewModel]: List of reviews by the user

        Raises:
            UserNotFound: If user does not exist
        """
        # Validate user exists
        user = await self.user_repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFound()

        reviews = await self.review_repository.get_reviews_by_user(
            user_uid=user.uid, limit=limit, offset=offset
        )

        return [ReviewModel.model_validate(review) for review in reviews]

    async def update_review(
        self,
        review_uid: str,
        user_email: str,
        review_data: ReviewUpdateModel,
    ) -> ReviewModel:
        """
        Update a review

        Args:
            review_uid: UID of the review to update
            user_email: Email of the user updating the review
            review_data: Updated review data

        Returns:
            ReviewModel: Updated review

        Raises:
            ReviewNotFound: If review does not exist
            UserNotFound: If user does not exist
            UnauthorizedReviewAccess: If user does not own the review
        """
        # Get the review
        review = await self.review_repository.get_review_by_uid(UUID(review_uid))
        if not review:
            raise ReviewNotFound()

        # Validate user owns the review
        user = await self.user_repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFound()

        if review.user_uid != user.uid:
            raise UnauthorizedReviewAccess()

        # Update the review
        updated_review = await self.review_repository.update_review(
            review_uid=UUID(review_uid), review_data=review_data
        )

        logger.info(f"User {user_email} updated review {review_uid}")
        return ReviewModel.model_validate(updated_review)

    async def delete_review(
        self,
        review_uid: str,
        user_email: str,
    ) -> bool:
        """
        Delete a review

        Args:
            review_uid: UID of the review to delete
            user_email: Email of the user deleting the review

        Returns:
            bool: True if deleted successfully

        Raises:
            ReviewNotFound: If review does not exist
            UserNotFound: If user does not exist
            UnauthorizedReviewAccess: If user does not own the review
        """
        # Get the review
        review = await self.review_repository.get_review_by_uid(UUID(review_uid))
        if not review:
            raise ReviewNotFound()

        # Validate user owns the review
        user = await self.user_repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFound()

        if review.user_uid != user.uid:
            raise UnauthorizedReviewAccess()

        # Delete the review
        deleted = await self.review_repository.delete_review(UUID(review_uid))

        logger.info(f"User {user_email} deleted review {review_uid}")
        return deleted

    async def get_book_rating_stats(
        self,
        book_uid: str,
    ) -> BookRatingStatsModel:
        """
        Get rating statistics for a book

        Args:
            book_uid: UID of the book

        Returns:
            BookRatingStatsModel: Statistics including total reviews and average rating

        Raises:
            BookNotFound: If book does not exist
        """
        # Validate book exists
        book = await self.book_repository.get_book(UUID(book_uid))
        if not book:
            raise BookNotFound()

        total_reviews = await self.review_repository.count_reviews_by_book(book_uid=UUID(book_uid))

        average_rating = await self.review_repository.get_average_rating_by_book(
            book_uid=UUID(book_uid)
        )

        return BookRatingStatsModel(
            book_uid=UUID(book_uid),
            total_reviews=total_reviews,
            average_rating=average_rating or 0.0,
        )
