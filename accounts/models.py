from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_plugged = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_bot = models.BooleanField(verbose_name='robot', default=False)

    username = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.username
