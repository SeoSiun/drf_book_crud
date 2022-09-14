from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    # 일반 유저 생성
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have email')
        user = self.model(
            email = self.normalize_email(email),
            name = extra_fields.get('name'),
            address = extra_fields.get('address'),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password = password,
            name = extra_fields.get('name'),
            address = extra_fields.get('address'),
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, null=False,unique=True)
    name = models.CharField(max_length=100, null=True, default=None, blank=True)
    address = models.CharField(max_length=200, null=True, default=None, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    objects= UserManager()
    