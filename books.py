from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "title one", "author": "author one", "category": "math"},
    {"title": "title two", "author": "author two", "category": "english"},
    {"title": "title three", "author": "author three", "category": "hindi"}
]


@app.get("/get-all-books")
async def read_all_books():
    return BOOKS


@app.get("/books/{dynamic_param}")
async def read_all_book(dynamic_param: str):
    for book in BOOKS:
        if book.get("title") == dynamic_param:
            return {"dynamic_param": "yehhhhhhhhh"}


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def get_book_by_author_and_category(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold() and \
                book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book/{book_title}")
async def update_book(book_title: str, update_book_data=Body()):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            book["category"] = update_book_data["category"]
            book["author"] = update_book_data["author"]


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

    return "Done"
