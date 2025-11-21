from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.models.reviews import Review
from src.presentation.web.schemas.reviews import ReviewCreateModel, ReviewUpdateModel


class IReviewRepository(ABC):
    """Interface for review repository operations"""

    @abstractmethod
    async def create_review(
        self, review_data: ReviewCreateModel, user_uid: UUID, book_uid: UUID
    ) -> Review:
        """Create a new review"""

    @abstractmethod
    async def get_review_by_uid(self, review_uid: UUID) -> Optional[Review]:
        """Get a review by its UID"""

    @abstractmethod
    async def get_all_reviews(self, limit: int = 100, offset: int = 0) -> List[Review]:
        """Get all reviews with pagination"""

    @abstractmethod
    async def get_reviews_by_book(
        self, book_uid: UUID, limit: int = 100, offset: int = 0
    ) -> List[Review]:
        """Get all reviews for a specific book"""

    @abstractmethod
    async def get_reviews_by_user(
        self, user_uid: UUID, limit: int = 100, offset: int = 0
    ) -> List[Review]:
        """Get all reviews by a specific user"""

    @abstractmethod
    async def update_review(
        self, review_uid: UUID, review_data: ReviewUpdateModel
    ) -> Optional[Review]:
        """Update an existing review"""

    @abstractmethod
    async def delete_review(self, review_uid: UUID) -> bool:
        """Delete a review by UID"""

    @abstractmethod
    async def user_has_reviewed_book(self, user_uid: UUID, book_uid: UUID) -> bool:
        """Check if user has already reviewed a book"""

    @abstractmethod
    async def get_average_rating_by_book(self, book_uid: UUID) -> Optional[float]:
        """Get average rating for a book"""

    @abstractmethod
    async def review_exists(self, review_uid: UUID) -> bool:
        """Check if a review exists by UID"""
