from django.contrib import admin
from books.models import Book, Rent


# Register your models here.

admin.site.register(Book)
admin.site.register(Rent)