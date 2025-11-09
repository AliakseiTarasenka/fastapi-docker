import uuid
from datetime import datetime
from typing import List

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel, Relationship


class BookTag(SQLModel, table=True):
    __tablename__ = "book_tags"
    book_uid: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_uid: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
