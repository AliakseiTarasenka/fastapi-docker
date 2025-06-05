from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid


class Book(SQLModel, table=True):
    """
    Schema definition for books based on SQLModel ORM
    """

    __tablename__ = "books"
    # sa_column lets you directly use a SQLAlchemy Column object to define advanced database-specific behaviors.
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: Optional[datetime] = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
