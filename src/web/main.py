from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.db.database import init_db
from src.web.routes.books import app as books_router
from src.web.routes.auth import app as auth_router
from src.web.routes.users import app as users_router
from src.service.errors import register_all_errors


# create connection to the database
# use context manager for connection to the database

# the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Decorator to async context manager.:

    operations to execute prior to the application receiving requests,
    as well as when it concludes receiving them
    # https://fastapi.tiangolo.com/advanced/events/
    """
    print("Server is starting...")
    await init_db()
    yield
    print("Server is stopping")


version = "v1"
app = FastAPI(
    debug=True,
    title="Books",
    description="A RESTful API for books web service",
    version=version,
    lifespan=lifespan,
)
app.include_router(books_router, prefix=f"/api/{version}", tags=["books"])
app.include_router(users_router, prefix=f"/api/{version}", tags=["users"])
app.include_router(auth_router, prefix=f"/api/{version}", tags=["auth"])
register_all_errors(app) # need to register issue execution while processing the API