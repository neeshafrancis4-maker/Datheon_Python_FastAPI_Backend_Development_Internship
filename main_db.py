from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- Hissa 1: Database se connection ---
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)


Base.metadata.create_all(bind=engine)


# --- Hissa 2: Pydantic classes (API ka data) ---
class BookCreate(BaseModel):
    title: str
    author: str
    price: float


class BookOut(BookCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- App ---
app = FastAPI(title="BookStore API with SQLite")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- GET: books parhna ---
@app.get("/books", response_model=list[BookOut])
def get_books(author: str | None = None, db: Session = Depends(get_db)):
    query = db.query(BookDB)
    if author:
        query = query.filter(BookDB.author == author)
    return query.all()


# --- POST: nayi book add karna ---
@app.post("/books", response_model=BookOut, status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookDB(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# --- Hissa 3: PUT: book update karna ---
@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated: BookCreate, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = updated.title
    book.author = updated.author
    book.price = updated.price
    db.commit()
    db.refresh(book)
    return book


# --- DELETE: book hatana ---
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Deleted"}