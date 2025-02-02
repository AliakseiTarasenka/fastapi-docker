from fastapi import FastAPI
from pyjobs.web.api.api import router as jobs_router
from contextlib import asynccontextmanager

# the lifespan event
@asynccontextmanager
async def lifespan(server: FastAPI):
    print("Server is starting...")
    yield
    print("server is stopping")

version = "v1"
server = FastAPI(debug=True,
                 title='Jobs',
                 description='A RESTful API for a Jobs review web service',
                 version=version,
                 lifespan=lifespan
                 )
server.include_router(jobs_router, prefix=f"/api/{version}", tags=['jobs'])