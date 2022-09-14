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
        fields = ['user', 'book']
