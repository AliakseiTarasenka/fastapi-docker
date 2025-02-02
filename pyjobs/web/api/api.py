import uuid
from copy import deepcopy
from datetime import datetime, date, timezone, timedelta
from itertools import islice
from typing import Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import conint
from starlette import status
from starlette.responses import Response

from pyjobs.web.api.schemas import GetJobSchema, ListJobsSchema, CreateJobSchema, ContractTypeEnum, SortByEnum

router = APIRouter()


jobs = [
    {
        "title": "Python developer",
        "rate": {
            "amount": 100,
            "amountPerTime": "day",
            "currency": "USD"
        },
        "benefits": "Work from Home",
        "location": {
            "city": "Warsaw",
            "state": None,
            "country": "Poland"
        },
        "hirer": "PyJobs",
        "contractType": "contract",
        "description": "Python dev",
        "skills": [
            "Python.core",
            "FastAPI"
        ],
        "liveUntil": (datetime.now(timezone.utc) + timedelta(days=30)),
        "id": uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        "dateListed": datetime.now(timezone.utc),
        "visible": True
    }
]


@router.get('/get_headers')
async def get_all_request_headers(
        user_agent: Optional[str] = Header(None),
        accept_encoding: Optional[str] = Header(None),
        referer: Optional[str] = Header(None),
        connection: Optional[str] = Header(None),
        accept_language: Optional[str] = Header(None),
        host: Optional[str] = Header(None),
):
    request_headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
        "Referer": referer,
        "Accept-Language": accept_language,
        "Connection": connection,
        "Host": host
    }

    return request_headers


@router.get("/jobs", response_model=ListJobsSchema)
async def get_jobs(
        dateSincePosted: Optional[date] = None,
        contractType: Optional[ContractTypeEnum] = None,
        page: conint(ge=1) = 1,
        perPage: conint(ge=1, le=100) = 1,
        sortBy: SortByEnum = SortByEnum.datePosted
):
    jobs_list = [job for job in jobs if job["visible"]]
    if dateSincePosted:
        jobs_list = [job for job in jobs if job["dateSincePosted"] >= dateSincePosted]
    if contractType:
        jobs_list = [job for job in jobs if job["contractType"] == contractType]
    jobs_list = sorted(
        jobs_list,
        key=lambda job: job["dateListed"] if sortBy == SortByEnum.datePosted else job["rate"]["amount"]
    )
    page = page - 1
    start = perPage * page if page > 0 else page
    stop = start + perPage
    return {
        "jobs": list(islice(jobs_list, start, stop)),
        "pages": (len(jobs_list) / perPage) if len(jobs_list) > perPage else 1,
    }


@router.post("/jobs", response_model=GetJobSchema, status_code=status.HTTP_201_CREATED)
async def create_job(job_details: CreateJobSchema):
    job = job_details.dict()
    job["id"] = uuid.uuid4()
    job["location"] = {
        "city": "London",
        "state": None,
        "country": "UK",
    }
    job["dateListed"] = datetime.now(timezone.utc)
    job["hirer"] = "PyJobs.works"
    job["visible"] = True
    jobs.append(job)
    return job


@router.get("/jobs/{job_id}", response_model=GetJobSchema)
async def get_job(job_id: uuid.UUID):
    for job in jobs:
        if job["id"] == job_id:
            return job
    raise HTTPException(
        status_code=404, detail=f"Job listing with ID {job_id} not found"
    )


@router.put("/jobs/{job_id}", response_model=GetJobSchema)
async def update_job(job_id: uuid.UUID, job_details: CreateJobSchema):
    for job in jobs:
        if job["id"] == job_id:
            job["title"] = job_details.title
            job["rate"] = job_details.rate
            job["benefits"] = job_details.benefits
            job["location"] = {
                "city": "London",
                "country": "UK",
                "state": None,
            }
            job["hirer"] = "PyJobs.works"
            job["contractType"] = job_details.contractType.value
            job["description"] = job_details.description
            job["skills"] = job_details.skills
            job["liveUntil"] = job_details.liveUntil
            return job
    raise HTTPException(
        status_code=404, detail=f"Job listing with ID {job_id} not found"
    )


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_job(job_id: uuid.UUID):
    for index, job in enumerate(jobs):
        if job["id"] == job_id:
            jobs.pop(index)
            return
    raise HTTPException(
        status_code=404, detail=f"Job listing with ID {job_id} not found"
    )


@router.post("/jobs/{job_id}/cancel", response_model=GetJobSchema, status_code=status.HTTP_201_CREATED)
async def cancel_job(job_id: uuid.UUID):
    for job in jobs:
        if job["id"] == job_id:
            job["visible"] = False
            return job
    raise HTTPException(
        status_code=404, detail=f"Job listing with ID {job_id} not found"
    )


@router.post("/jobs/{job_id}/reactivate", response_model=GetJobSchema, status_code=status.HTTP_201_CREATED)
async def reactivate_job(job_id: uuid.UUID):
    for job in jobs:
        if job["id"] == job_id:
            job["visible"] = True
            return job
    raise HTTPException(
        status_code=404, detail=f"Job listing with ID {job_id} not found"
    )
