from django.contrib import admin

# Register your models here.

from .models import Book, Genre

admin.site.register(Genre)
admin.site.register(Book)
