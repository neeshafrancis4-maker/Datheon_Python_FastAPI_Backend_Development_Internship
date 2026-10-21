# Datheon Python + FastAPI Backend Development Internship

Two REST API projects built with FastAPI.

## Task 1: BookStore REST API with Pydantic Validation (main.py)
- GET /books: list books (optional filter: ?author=Name)
- POST /books: add a book
- PUT /books/{book_id}: update a book
- DELETE /books/{book_id}: delete a book
- Pydantic validation, status codes, 404 error handling
- Data is stored in memory (resets on restart)

Run: python -m uvicorn main:app --reload

## Task 3: Database Persistence with SQLAlchemy and SQLite (main_db.py)
- Same CRUD endpoints, backed by a SQLite database (books.db)
- SQLAlchemy ORM model (BookDB), Pydantic schemas (BookCreate, BookOut)
- Database session handled with FastAPI dependency injection
- Data persists after server restart

Run: python -m uvicorn main_db:app --reload

## Setup
1. pip install -r requirements.txt
2. Run either app with the commands above
3. Open http://127.0.0.1:8000/docs for the Swagger UI

## Tech stack
Python 3, FastAPI, Uvicorn, Pydantic, SQLAlchemy, SQLite