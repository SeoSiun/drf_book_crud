from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    # 일반 유저 생성
    def create_user(self, email, name, address, password=None):
        if not email:
            raise ValueError('user must have email')
        if not name:
            raise ValueError('user must have name')
        if not address:
            raise ValueError('user must have address')
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            address = address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, address, password=None):
        user = self.create_user(
            email,
            password = password,
            name = name,
            address = address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, null=False,unique=True)
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username
