from fastapi import FastAPI

from pyjobs.web.api.api import router as jobs_router

version = "v1"
name = "Jobs"
server = FastAPI(debug=True,
                 title=name,
                 description=f"A RESTful API for a {name} review web service",
                 version=version)

server.include_router(jobs_router, prefix=f"/api/{version}", tags=[name])
