from pydantic import BaseModel
import uuid
from datetime import datetime, date
from src.reviews.schemas import ReviewModel
from typing import List
from src.tags.schemas import TagModel

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True


class BookDetailModel(Book):
    reviews: List[ReviewModel]
    tags: List[TagModel]
    

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


# class BookBase(BaseModel):
#     title: str
#     author: str
#     publisher: str
#     page_count: int
#     language: str

# class BookCreate(BookBase):
#     published_date: str


# class BookUpdate(BookBase):
#     pass

# class Book(BookBase):
#     id: uuid.UUID
#     created_at: datetime
#     updated_at: datetime