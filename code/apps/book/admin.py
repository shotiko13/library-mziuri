from django.contrib import admin

from .models import Book, Genre, Borrow

# Register your models here.

admin.site.register(Book)


admin.site.register(Genre)

admin.site.register(Borrow)