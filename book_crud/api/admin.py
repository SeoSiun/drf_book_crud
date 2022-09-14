from django.contrib import admin
from .models import Book, Order


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'introduction', 'price', 'user']
    list_display_links = ['id', 'title']
    list_editable = ['introduction']
    list_per_page = 10
    list_filter = ['price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
    list_display = ['user', 'book', 'created_at']
    list_per_page = 10
