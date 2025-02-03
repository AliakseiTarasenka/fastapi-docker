from fastapi import FastAPI
from pyjobs.web.api.api import router as jobs_router
from contextlib import asynccontextmanager
from pyjobs.persistence.database import initdb

# the lifespan event
@asynccontextmanager
async def lifespan(server: FastAPI):
    """Decorator to async context manager."""
    print("Server is starting...")
    await initdb()
    yield
    print("Server is stopping")

version = "v1"
server = FastAPI(debug=True,
                 title='Jobs',
                 description='A RESTful API for a Jobs review web service',
                 version=version,
                 lifespan=lifespan
                 )
server.include_router(jobs_router, prefix=f"/api/{version}", tags=['jobs'])