from django.db import models
from user.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=30)
    introduction = models.CharField(max_length=500)
    price = models.IntegerField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    is_on_sale = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
