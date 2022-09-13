from rest_framework import viewsets, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, Token
from .serializers import UserSerializer

class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary='유저 생성 (회원가입)',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password', 'name', 'address'],
        ),
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        '''email, password, name, address 정보를 갖는 유저 생성 (email 중복 불가) / 해당 유저의 token을 반환함.'''
        user = User.objects.create_user(
            email=request.data['email'],
            name=request.data['name'],
            address=request.data['address'],
            password=request.data['password']
        )
        user.save()
        return Response({
            'token': Token.objects.create(user=user).key
        }, status=HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_summary='로그인',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password'],
        ),
        responses={
            HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    @action(detail=False, methods=['POST'])
    @permission_classes((AllowAny,))
    def login(self, request):
        '''email, password와 일치하는 유저의 token을 반환'''
        user = authenticate(email=request.data['email'], password=request.data['password'])

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({ 'token': token.key }, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)
