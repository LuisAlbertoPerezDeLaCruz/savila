from django.db import models
from accounts.models import User


class Game(models.Model):
    STATUSES = (
        ("S", "Started"),
        ("A", "Active"),
        ("I", "Inactive"),
        ("C", "Completed"),
        ("X", "Expired"),
    )
    name = models.CharField(max_length=30, unique=True)
    status = models.CharField(
        choices=STATUSES, max_length=1, blank=False, verbose_name="Status", default='S')

    created_by = models.ForeignKey(
        User, null=True, related_name='games', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
