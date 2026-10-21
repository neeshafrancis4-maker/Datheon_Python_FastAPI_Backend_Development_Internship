from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="BookStore API")

class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float

books: list[Book] = []

@app.get("/books")
def get_books(author: str | None = None):
    if author:
        return [b for b in books if b.author == author]
    return books

@app.post("/books", status_code=201)
def add_book(book: Book):
    books.append(book)
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated: Book):
    for i, b in enumerate(books):
        if b.id == book_id:
            books[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, b in enumerate(books):
        if b.id == book_id:
            books.pop(i)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Book not found")