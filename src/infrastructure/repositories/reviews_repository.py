from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.reviews import Review
from src.domain.repositories.reviews_repository_interface import IReviewRepository
from src.presentation.web.schemas.reviews import ReviewCreateModel, ReviewUpdateModel


class ReviewRepository(IReviewRepository):
    """Concrete implementation of review repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(
        self, review_data: ReviewCreateModel, user_uid: UUID, book_uid: UUID
    ) -> Review:
        """Create a new review"""
        review_dict = review_data.model_dump()
        new_review = Review(**review_dict, user_uid=user_uid, book_uid=book_uid)

        self.session.add(new_review)
        await self.session.commit()
        await self.session.refresh(new_review)

        return new_review

    async def get_review_by_uid(self, review_uid: UUID) -> Optional[Review]:
        """Get a review by its UID"""
        statement = select(Review).where(Review.uid == review_uid)
        result = await self.session.exec(statement)
        return result.first()

    async def get_all_reviews(self, limit: int = 100, offset: int = 0) -> List[Review]:
        """Get all reviews with pagination"""
        statement = select(Review).order_by(desc(Review.created_at)).limit(limit).offset(offset)
        result = await self.session.exec(statement)
        return result.all()

    async def get_reviews_by_book(
        self, book_uid: UUID, limit: int = 100, offset: int = 0
    ) -> List[Review]:
        """Get all reviews for a specific book"""
        statement = (
            select(Review)
            .where(Review.book_uid == book_uid)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.exec(statement)
        return result.all()

    async def get_reviews_by_user(
        self, user_uid: UUID, limit: int = 100, offset: int = 0
    ) -> List[Review]:
        """Get all reviews by a specific user"""
        statement = (
            select(Review)
            .where(Review.user_uid == user_uid)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.exec(statement)
        return result.all()

    async def update_review(
        self, review_uid: UUID, review_data: ReviewUpdateModel
    ) -> Optional[Review]:
        """Update an existing review"""
        review = await self.get_review_by_uid(review_uid)

        if not review:
            return None

        update_data = review_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(review, key, value)

        review.updated_at = datetime.now()

        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(review)

        return review

    async def delete_review(self, review_uid: UUID) -> bool:
        """Delete a review by UID"""
        review = await self.get_review_by_uid(review_uid)

        if not review:
            return False

        await self.session.delete(review)
        await self.session.commit()

        return True

    async def user_has_reviewed_book(self, user_uid: UUID, book_uid: UUID) -> bool:
        """Check if user has already reviewed a book"""
        statement = select(Review).where(Review.user_uid == user_uid, Review.book_uid == book_uid)
        result = await self.session.exec(statement)
        return result.first() is not None

    async def get_average_rating_by_book(self, book_uid: UUID) -> Optional[float]:
        """Get average rating for a book"""
        statement = select(func.avg(Review.rating)).where(Review.book_uid == book_uid)
        result = await self.session.exec(statement)
        avg_rating = result.one()

        return round(avg_rating, 2) if avg_rating else None

    async def review_exists(self, review_uid: UUID) -> bool:
        """Check if a review exists by UID"""
        statement = select(Review.uid).where(Review.uid == review_uid)
        result = await self.session.exec(statement)
        return result.first() is not None
