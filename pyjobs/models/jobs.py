from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import List, Optional


class Rate(SQLModel, table=True):
    __tablename__ = "rates"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: int = Field(sa_column=Column(pg.INTEGER))
    amountPerTime: str = Field(sa_column=Column(pg.VARCHAR))
    currency: str = Field(sa_column=Column(pg.VARCHAR))
    job_id: uuid.UUID = Field(default=uuid.uuid4, foreign_key="job.id")

    def __repr__(self) -> str:
        return f"<Rate: id={self.id}, amount={self.amount}, amountPerTime={self.amountPerTime}, currency={self.currency}>"


class Location(SQLModel, table=True):
    __tablename__ = "locations"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    city: str = Field(sa_column=Column(pg.VARCHAR))
    state: str = Field(sa_column=Column(pg.VARCHAR))
    country: str = Field(sa_column=Column(pg.VARCHAR))
    job_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="job.id")

    def __repr__(self) -> str:
        return f"<Location: id={self.id}, city={self.city}, state={self.state}, country={self.country}>"


class Skill(SQLModel, table=True):
    __tablename__ = "skills"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    skill: str = Field(sa_column=Column(pg.VARCHAR))
    job_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="job.id")

    def __repr__(self) -> str:
        return f"<Skill: id={self.id}, skill={self.skill}>"


class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False
        )
    )
    title: str = Field(sa_column=Column(pg.VARCHAR))
    benefits: str = Field(sa_column=Column(pg.TEXT))
    hirer: str = Field(sa_column=Column(pg.VARCHAR))
    contractType: str = Field(sa_column=Column(pg.VARCHAR))
    description: str = Field(sa_column=Column(pg.VARCHAR))
    liveUntil: str = Field(sa_column=Column(pg.TIMESTAMP))
    dateListed: str = Field(sa_column=Column(pg.TIMESTAMP))
    visible: int = Field(sa_column=Column(pg.INTEGER))

    rate: Optional[Rate] = Relationship(back_populates="job")
    location: Optional[Location] = Relationship(back_populates="job")
    skills: List[Skill] = Relationship(back_populates="job")

    def __repr__(self) -> str:
        return f"<Job: id={self.id}, title={self.title}, description={self.description}>"


# Establishing reverse relationships
Rate.job = Relationship(back_populates="rate")
Location.job = Relationship(back_populates="location")
Skill.job = Relationship(back_populates="skills")
