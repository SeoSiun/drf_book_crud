from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Book
from .serializers import BookSerializer


def is_valid_ordering(ordering):
    if ordering == 'title' or ordering == '-title' \
            or ordering == 'author' or ordering == '-author' \
            or ordering == 'price' or ordering == '-price':
        return True
    return False

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        search_title = self.request.query_params.get('title', )
        search_author = self.request.query_params.get('author', )
        ordering = self.request.query_params.get('ordering',)

        if search_title:
            qs = qs.filter(title__contains=search_title)
        if search_author:
            qs = qs.filter(author__contains=search_author)
        if is_valid_ordering(ordering):
            return qs.order_by(ordering)

        return qs

    @swagger_auto_schema(
        operation_summary='책 목록',
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        """query parameter가 없다면 전체 목록, 있다면 query로 받은 title, author를 포함하는 책 목록을 가져옴."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary='책 생성')
    def create(self, request, *args, **kwargs):
        """title, author, introduction, price 정보를 갖는 책 생성."""
        return super(BookViewSet, self).create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 detail 정보')
    def retrieve(self, request, *args, **kwargs):
        """id에 해당하는 책의 정보를 가져옴."""
        return super(BookViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 정보 전체 수정')
    def update(self, request, *args, **kwargs):
        """id에 해당하는 책의 title, author, introduction, price를 request로 받은 값으로 수정"""
        return super(BookViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 정보 수정')
    def partial_update(self, request, *args, **kwargs):
        """id에 해당하는 책의 title, author, introduction, price 중 request body에서 받은 값을 수정"""
        return super(BookViewSet, self).partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 삭제')
    def destroy(self, request, *args, **kwargs):
        """id에 해당하는 책을 삭제"""
        return super(BookViewSet, self).destroy(request, *args, **kwargs)