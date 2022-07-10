import json
from django.db import models
from accounts.models import User
from datetime import datetime


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

    last_play_at = models.DateTimeField(null=True)

    last_play_by = models.ForeignKey(
        User, related_name='last_plays', null=True, on_delete=models.CASCADE)
    next_play_by = models.ForeignKey(
        User, related_name='next_plays', null=True, on_delete=models.CASCADE)

    turns_played = models.IntegerField(default=0)

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
    game_player = models.ForeignKey(
        GamePlayer, null=True, related_name='gameplayers', on_delete=models.CASCADE)
    value_played = models.DecimalField(
        decimal_places=2, default=0, max_digits=12,
    )

    turn_result = models.CharField(max_length=500)

    def set_turn_result(self, value):
        self.turn_result = json.dumps(value)

    def get_turn_result(self):
        return json.loads(self.turn_result)

    def save(self,  *args, **kwargs):
        self.game_player.last_play_at = datetime.now()

        # Si el objecto self no esta creado, entonces el pk en nulo,
        # lo cual quiere decir que estoy creando el objeto y
        # no actualizandolo

        if self.pk is None:
            self.turn += 1
            # A traves del la relacion game_player modifico el objeto game
            # adicionandole loa valores: last_play_at, last_play_by, next_play_by
            # y turns_played

            self.game_player.game.last_play_at = datetime.now()
            self.game_player.game.turns_played = self.turn
            self.game_player.game.last_play_by = self.game_player.player

            _ = self.game_player.game.playerslist().strip().split()
            curr_idx = _.index(self.game_player.player.username)
            next_idx_ = curr_idx + 1

            if next_idx_ > len(_)-1:
                next_idx = 0
            else:
                next_idx = next_idx_

            next_player = User.objects.get(username=_[next_idx])

            self.game_player.game.next_play_by = next_player
            self.game_player.game.save()
        else:
            # Automaticamente calculo los turns_played, buscando los turns que
            # pertenecen al mismo game
            turns_played = self.__class__.objects.filter(
                game_player__game=self.game_player.game).count()
            self.game_player.game.turns_played = turns_played
            self.game_player.game.save()

        self.game_player.save()
        super().save(*args,  **kwargs)

    def __str__(self):
        return f'{self.turn},{self.game_player.player.username}, {self.value_played}, {self.turn_result}'


class TokenForRefresh(models.Model):
    token = models.CharField(max_length=30)

    def __str__(self):
        return self.token
