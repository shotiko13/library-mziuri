from ninja import Query, Router, Schema
from django.db.models import Model
from django.shortcuts import get_object_or_404
import json

from .models import Book, Genre, Borrow
from .serializers import (
    BookSchema,
    BookCreateSchema, 
    BookUpdateSchema, 
    BorrowSchema, 
    BorrowCreateSchema
)

from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

router = Router()

from django.db.models import Q
from ninja import Query
from typing import Optional

class BookFilter(Schema):
    genre: Optional[str] = None
    borrowed_by: Optional[str] = None
    borrowed: Optional[bool] = None



"""AUTH ROUTER"""

auth_router = Router()

@auth_router.post("/token")
def get_token(request, username: str, password: str):
    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    return {"error": "Invalid credentials"}, 401

from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
            return user
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None
"""AUTH ROUTER"""


@router.get("/books", auth=JWTBearer())
def get_books(request, filters: BookFilter = Query(...)):
    books = Book.objects.all()

    if filters.genre:
        books = books.filter(genres__name=filters.genre)
    
    if filters.borrowed_by:
        books = books.filter(genres__borrowed_by=filters.borrowed_by)

    if filters.borrowed is not None:
        books = books.filter(borrowed_by__isnull=filters.borrowed_by)

    if books:
        return [BookSchema.from_orm(book) for book in books]
    else:
        return {
            "result": "არ მოიძებნა"
        }

@router.get("/books/{book_id}", response=BookSchema)
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)

@router.post("/books", response=BookSchema)
def create_book(request, payload: BookCreateSchema):
    book = Book.objects.create(
        title=payload.title,
        author=payload.author,
        published_date=payload.published_date,
    )
    book.genres.set(Genre.objects.filter(id__in=payload.genre_ids))
    return book

@router.put("/books/{book_id}", response=BookSchema)
def update_book(request, book_id: int, payload: BookUpdateSchema):
    book = get_object_or_404(Book, id=book_id)

    if payload.title:
        book.title = payload.title
    if payload.author:
        book.author = payload.author
    if payload.published_date:
        book.published_date = payload.published_date
    if payload.genre_ids:
        book.genres.set(Genre.objects.filter(id__in=payload.genre_ids))
    
    book.save()

    return book

@router.delete("books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"response": "book deleted successfully"}

@router.post("books/{book_id}/borrow", response=BookSchema)
def borrow_book(request, book_id: int, payload: BorrowCreateSchema):
    book = get_object_or_404(Book, id=book_id)

    if book.borrowed_by:
        return {"Error": "Book is already borrowed"}
    book.borrow(payload.person)
    return book

@router.post("books/{book_id}/return")
def return_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    
    if not book.borrowed_by:
        return {"message": "book is not taken"}
    
    book.return_book()
    return {"message": "book is returned"}