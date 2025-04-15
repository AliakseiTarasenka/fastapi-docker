from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional

class BookCreateModel(BaseModel):
    title: str
    author: str

app = FastAPI()

@app.post("/book")
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/greet")
async def greet(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}

# request query parameter: http://127.0.0.1:8000/greet?age=10
# request path parameter: http://127.0.0.1:8000/greet/{name}


@app.get("/headers")
async def headers(
        user_agent: Optional[str] = Header(None),
        accept_encoding: Optional[str] = Header(None),
        referer: Optional[str] = Header(None),
        connection: Optional[str] = Header(None),
        accept_language: Optional[str] = Header(None),
        host: Optional[str] = Header(None)):
     request_headers = {}
     request_headers["User-Agent"] = user_agent
     request_headers["Accept-Encoding"] = accept_encoding
     request_headers["Referer"] = referer
     request_headers["Accept-Language"] = accept_language
     request_headers["Connection"] = connection
     request_headers["Host"] = host

     return request_headers