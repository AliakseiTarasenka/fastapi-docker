from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
# AKA Data Transfer Objects, where we can specify data types for our objects
from pydantic import BaseModel, confloat, conlist, conint, Extra


class AmountPerTimeEnum(Enum):
    hour = "hour"
    day = "day"
    month = "month"
    year = "year"


class Rate(BaseModel):
    amount: confloat(ge=1)
    amountPerTime: AmountPerTimeEnum
    currency: str


class Location(BaseModel):
    city: str
    state: Optional[str]
    country: str


class ContractTypeEnum(Enum):
    contract = "contract"
    permanent = "permanent"


class GetJobSchema(BaseModel):
    id: UUID
    title: str
    dateListed: datetime
    rate: Rate
    benefits: str
    location: Location
    hirer: str
    contractType: ContractTypeEnum
    skills: conlist(str)
    liveUntil: datetime

    def dict(
        self,
        *args,
        **kwargs
    ) -> 'DictStrAny':
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)


class ListJobsSchema(BaseModel):
    jobs: list[GetJobSchema]
    pages: conint(ge=1)


class CreateJobSchema(BaseModel):
    title: str
    rate: Rate
    benefits: str
    location: UUID
    hirer: UUID
    contractType: ContractTypeEnum
    description: str
    skills: conlist(str)
    liveUntil: datetime


class SortByEnum(Enum):
    datePosted = "datePosted"
    rate = "rate"
