import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ReviewCreateModel(BaseModel):
    """Schema for creating a new review"""

    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    review_text: str = Field(..., min_length=1, max_length=2000, description="Review content")

    @field_validator("review_text")
    @classmethod
    def validate_review_text(cls, text: str) -> str:
        """Validate and clean review text"""
        text = text.strip()
        if not text:
            raise ValueError("Review text cannot be empty")
        return text


class ReviewUpdateModel(BaseModel):
    """Schema for updating an existing review"""

    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating between 1 and 5")
    review_text: Optional[str] = Field(
        None, min_length=1, max_length=2000, description="Review content"
    )

    @field_validator("review_text")
    @classmethod
    def validate_review_text(cls, text: Optional[str]) -> Optional[str]:
        """Validate and clean review text"""
        if text is not None:
            text = text.strip()
            if not text:
                raise ValueError("Review text cannot be empty")
        return text


class ReviewModel(BaseModel):
    """Schema for review response"""

    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: uuid.UUID
    book_uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "rating": 5,
                "review_text": "Excellent book! Highly recommend.",
                "user_uid": "123e4567-e89b-12d3-a456-426614174001",
                "book_uid": "123e4567-e89b-12d3-a456-426614174002",
                "created_at": "2025-10-29T12:00:00",
                "updated_at": "2025-10-29T12:00:00",
            }
        },
    }


class BookRatingStatsModel(BaseModel):
    """Schema for book rating statistics"""

    book_uid: uuid.UUID
    total_reviews: int
    average_rating: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "book_uid": "123e4567-e89b-12d3-a456-426614174002",
                "total_reviews": 42,
                "average_rating": 4.35,
            }
        }
    }
