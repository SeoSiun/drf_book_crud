from rest_framework import viewsets, mixins

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
