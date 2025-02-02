from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class Job(SQLModel , table=True):
    __tablename__ = "jobs"

    id:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False
        )
    )
    title: str
    rate: int
    benefits: str
    location:int
    hirer: str
    contract_type: str
    description: str
    skills: str
    live_until: str
    date_listed: str
    visible: bool

    def __repr__(self) -> str:
        return f"<Job: id={self.id}, title={self.title}, description={self.description}>"