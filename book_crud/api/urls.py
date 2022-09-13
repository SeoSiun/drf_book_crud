from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet
from user.views import UserViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]