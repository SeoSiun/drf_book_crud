from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'introduction', 'price', 'user']
    list_display_links = ['id', 'title']
    list_editable = ['introduction']
    list_per_page = 10
    list_filter = ['price']
