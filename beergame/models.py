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

    def __players__(self):
        players_ = self.players
        players_str = ''
        for _ in players_:
            players_str += _.username
        return players_str

    def __str__(self):
        return self.name


class GamePlayer(models.Model):
    game = models.ForeignKey(
        Game, null=True, related_name='players', on_delete=models.CASCADE)
    player = models.ForeignKey(
        User, null=True, related_name='players', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_play_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.player.username}, {self.game.name}'
