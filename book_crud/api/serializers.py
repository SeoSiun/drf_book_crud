from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Book
        fields ='__all__'
