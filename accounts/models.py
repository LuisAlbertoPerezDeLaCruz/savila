from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)

    username = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.username
