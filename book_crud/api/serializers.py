from rest_framework import serializers

from .models import Book, Order


class BookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Book
        fields ='__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    book = serializers.ReadOnlyField(source='book.id')
    class Meta:
        model = Order
        fields = ['id', 'user', 'book', 'created_at']

class GetOrderSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')
    user_address = serializers.ReadOnlyField(source='user.address')
    book_id = serializers.ReadOnlyField(source='book.id')
    book_title = serializers.ReadOnlyField(source='book.title')
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'user_email', 'user_address', 'book_id', 'book_title', 'created_at']
