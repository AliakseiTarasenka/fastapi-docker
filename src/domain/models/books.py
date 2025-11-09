import uuid
from datetime import date, datetime
from typing import Optional, List

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel, Relationship

from src.domain.models.books_tags import BookTag, Tag


class Book(SQLModel, table=True):
    """Schema definition for books based on SQLModel ORM."""

    __tablename__ = "books"
    # sa_column lets you directly use a SQLAlchemy Column object to define advanced database-specific behaviors.
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
    tags: List["Tag"] = Relationship(
        link_model=BookTag,
        back_populates="book",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
