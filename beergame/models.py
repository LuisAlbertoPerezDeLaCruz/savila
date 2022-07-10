import json
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

    max_turns = models.IntegerField(default=25,)

    def playerslist(self):
        rels = self.players.all()
        players_str = ''
        for rel in rels:
            players_str += f'{rel.player.username} '
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

    class Meta:
        unique_together = ('game', 'player',)

    def __str__(self):
        return f'{self.player.username}, {self.game.name}'


class GameTurn(models.Model):
    turn = models.IntegerField(default=0,)
    player = models.ForeignKey(
        GamePlayer, null=True, related_name='gameplayers', on_delete=models.CASCADE)
    value_played = models.DecimalField(
        decimal_places=2, default=0, max_digits=12,
    )

    turn_result = models.CharField(max_length=500)

    def set_turn_result(self, value):
        self.turn_result = json.dumps(value)

    def get_turn_result(self):
        return json.loads(self.turn_result)

    def __str__(self):
        return f'{self.turn},{self.player.player.username}, {self.value_played}, {self.turn_result}'


class TokenForRefresh(models.Model):
    token = models.CharField(max_length=30)

    def __str__(self):
        return self.token
