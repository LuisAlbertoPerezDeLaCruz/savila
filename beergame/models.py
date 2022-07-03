from django.db import models
from accounts.models import User


class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)

    created_by = models.ForeignKey(
        User, related_name='games', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
