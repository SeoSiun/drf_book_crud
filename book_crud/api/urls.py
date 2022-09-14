from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, OrderViewSet
from user.views import UserViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]