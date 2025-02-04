from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

    def dict(
            self,
            *args,
            **kwargs
    ) -> 'DictStrAny':
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)

class BookUpdateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str