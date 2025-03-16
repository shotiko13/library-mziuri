from ninja import Schema
from datetime import datetime
from typing import List, Optional

class GenreSchema(Schema):
    id: int
    name: str
    description: str

class BookSchema(Schema):
    id: int
    title: str
    author: str
    published_date: Optional[datetime]
    genres: List[GenreSchema] = []
    borrowed_by: Optional[str]
    borrow_date: Optional[datetime]

class BookCreateSchema(Schema):
    title: str
    author: str
    published_date: Optional[datetime] = None
    genre_ids: List[int]

class BookUpdateSchema(Schema):
    title: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    genre_ids: Optional[List[int]] = None

class BorrowSchema(Schema):
    id: int
    person: str
    book: BookSchema
    date: datetime
    returned: bool

class BorrowCreateSchema(Schema):
    person: str
    book_id: int
