from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            address = validated_data['address'],
            password = validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['address', 'email', 'name', 'password']
