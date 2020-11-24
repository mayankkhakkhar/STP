from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=20000)
