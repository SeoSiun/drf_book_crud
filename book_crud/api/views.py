from rest_framework import viewsets, mixins, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Book, Order
from user.models import User
from .serializers import BookSerializer, OrderSerializer, GetOrderSerializer
from .permissions import IsOwnerOrReadOnly


def is_valid_ordering(ordering):
    if ordering == 'title' or ordering == '-title' \
            or ordering == 'author' or ordering == '-author' \
            or ordering == 'price' or ordering == '-price':
        return True
    return False

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        search_title = self.request.query_params.get('title', )
        search_author = self.request.query_params.get('author', )
        ordering = self.request.query_params.get('ordering',)
        user = self.request.user

        if search_title:
            qs = qs.filter(title__contains=search_title)
        if search_author:
            qs = qs.filter(author__contains=search_author)
        if user.is_active:
            qs = qs.filter(user__email=user)
        if is_valid_ordering(ordering):
            return qs.order_by(ordering)

        return qs

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @swagger_auto_schema(
        operation_summary='책 목록',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                              description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태, token이 주어지면 해당 유저가 생성한 책 목록을 가져옴.'),
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='값이 주어진다면 title에 이 값을 포함하는 책 목록을 가져옴.(검색어)'),
            openapi.Parameter('author', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='값이 주어진다면 author에 이 값을 포함하는 책 목록을 가져옴.(검색어)'),
            openapi.Parameter('ordering', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='이 값(field 이름)을 기준으로 오름차순으로 정렬 (field 명 앞에 "-"를 붙이면 내림차순) '
                                          + '/ 정렬 기준이 될 수 있는 field는 title, author, price '
                                          + '/ 올바르지 않은 값이 주어지거나, ordering을 넘기지 않으면 id를 기준으로 오름차순으로 정렬.'),
        ],
    )
    def list(self, request, *args, **kwargs):
        """query parameter에 따라 title, author로 검색하거나, title, author, price를 기준으로 정렬된 책 목록을 한 페이지(3개)씩 가져옴. / header로 토큰이 주어지면 해당 유저가 생성한 책 목록을 반환함."""
        return super(BookViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 생성', manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                          description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태.')
    ])
    def create(self, request, *args, **kwargs):
        """title, author, introduction, price 정보를 갖는 책 생성 / 로그인한 유저만 생성 가능"""
        return super(BookViewSet, self).create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 detail 정보')
    def retrieve(self, request, *args, **kwargs):
        """id에 해당하는 책의 정보를 가져옴."""
        return super(BookViewSet, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 정보 전체 수정', manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                          description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태.')
    ])
    def update(self, request, *args, **kwargs):
        """id에 해당하는 책의 title, author, introduction, price를 request로 받은 값으로 수정 / 해당 책을 생성한 유저만 가능"""
        return super(BookViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 정보 수정', manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                          description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태.')
    ])
    def partial_update(self, request, *args, **kwargs):
        """id에 해당하는 책의 title, author, introduction, price 중 request body에서 받은 값을 수정 / 해당 책을 생성한 유저만 가능"""
        return super(BookViewSet, self).partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='책 삭제', manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                          description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태.')
    ])
    def destroy(self, request, *args, **kwargs):
        """id에 해당하는 책을 삭제 / 해당 책을 생성한 유저만 가능"""
        return super(BookViewSet, self).destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_active:
            qs = qs.filter(user__email=user)

        return qs

    @swagger_auto_schema(
        operation_summary='주문 내역',
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                              description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태, 해당 유저의 주문 목록을 가져옴.'),
        ],
        responses={
            HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'next': openapi.Schema(type=openapi.FORMAT_URI),
                    'previous': openapi.Schema(type=openapi.FORMAT_URI),
                    'results': openapi.Schema(type=openapi.TYPE_OBJECT,
                                              properties={
                                                  'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                  'user_email': openapi.Schema(type=openapi.TYPE_STRING),
                                                  'user_address': openapi.Schema(type=openapi.TYPE_STRING),
                                                  'book_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                  'book_title': openapi.Schema(type=openapi.TYPE_STRING),
                                                  'created_at': openapi.Schema(type=openapi.FORMAT_DATETIME)
                                              }),
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        """token에 해당하는 유저의 주문 목록을 한 페이지(3개)씩 가져옴."""
        self.serializer_class = GetOrderSerializer
        return super(OrderViewSet, self).list(request, *args, **kwargs)


    def perform_create(self, serializer):
        [user] = User.objects.all().filter(id=self.request.user.id)
        [book] = Book.objects.all().filter(id=self.request.data['bookId'])

        book.is_on_sale=False
        book.save()
        serializer.save(user=user, book=book)


    @swagger_auto_schema(
        operation_summary='order생성 (주문하기)',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bookId': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['bookId'],
        ),
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING,
                              description='로그인/회원가입 결과 얻은 token, "Token {Token}" 형태.')
        ],
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'book': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'created_at': openapi.Schema(type=openapi.FORMAT_DATETIME)
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        '''token에 해당하는 유저와 bookId에 해당하는 책을 갖는 order 생성.'''
        return super(OrderViewSet, self).create(request, *args, **kwargs)


    def perform_destroy(self, instance):
        instance.book.is_on_sale = True
        instance.book.save()
        instance.delete()

    @swagger_auto_schema(operation_summary='order 삭제 (주문취소)')
    def destroy(self, request, *args, **kwargs):
        '''orderId에 해당하는 order 삭제'''
        return super(OrderViewSet, self).destroy(request, *args, **kwargs)
