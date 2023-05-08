from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    def __init__(self, id, title, description, rating):
        self.id = id
        self.title = title
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=3, max_length=120)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(1, "one title", "its is a good book", 5),
    Book(2, "two title", "its is a good book", 3),
    Book(3, "three title", "its is a good book", 4),
    Book(4, "four title", "its is a good book", 5)
]


@app.get("/")
async def read_all_books():
    return BOOKS


@app.post("/create-book/")
async def create_book(book_body: BookRequest):
    # convert type of request to object
    new_book = Book(**book_body.dict())
    new_book = assign_id(new_book)
    BOOKS.append(new_book)


def assign_id(book: Book):
    if len(BOOKS) == 0:
        book.id = 1
    else:
        book.id = BOOKS[-1].id + 1

    return book
