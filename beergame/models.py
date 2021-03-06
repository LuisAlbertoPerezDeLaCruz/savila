import json
from urllib import request
from django.db import models
from accounts.models import User


class Institution(models.Model):
    STATUSES = (
        ("A", "Active"),
        ("I", "Inactive"),
    )
    name = models.CharField(max_length=30, unique=True)

    status = models.CharField(
        choices=STATUSES, max_length=1, blank=False, default='A')

    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUSES = (
        ("A", "Active"),
        ("I", "Inactive"),
    )
    name = models.CharField(max_length=30, unique=True)

    institution = models.ForeignKey(
        Institution, null=True, related_name='courses', on_delete=models.CASCADE)

    instructor = models.ForeignKey(
        User, null=True, blank=True, related_name='courses', on_delete=models.CASCADE)

    status = models.CharField(
        choices=STATUSES, max_length=1, blank=False, default='A')

    def __str__(self):
        if self.instructor:
            r = f'{self.name}, {self.instructor.username}'
        else:
            r = f'{self.name} unassigned'
        return r


class Student(models.Model):
    STATUSES = (
        ("A", "Active"),
        ("I", "Inactive"),
    )

    user = models.ForeignKey(
        User, null=True, related_name='students', on_delete=models.CASCADE)

    course = models.ForeignKey(
        Course, null=True, related_name='students', on_delete=models.CASCADE)

    status = models.CharField(
        choices=STATUSES, max_length=1, blank=False, default='A')

    class Meta:
        unique_together = ('user', 'course',)

    def __str__(self):
        return f'{self.user.username}, {self.course.name}'


class Game(models.Model):
    STATUSES = (
        ("C", "Created"),
        ("S", "Started"),
        ("F", "Finished"),
        ("T", "Terminated"),
    )

    name = models.CharField(max_length=30, unique=True)

    status = models.CharField(
        choices=STATUSES, max_length=1, blank=False, default='C')

    created_by = models.ForeignKey(
        User, null=True, related_name='games', on_delete=models.CASCADE)

    institution = models.ForeignKey(
        Institution, null=True, related_name='games', on_delete=models.CASCADE)

    course = models.ForeignKey(
        Course, null=True, related_name='games', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    max_turns = models.IntegerField(default=25,)

    last_play_at = models.DateTimeField(null=True, blank=True)

    last_play_by = models.ForeignKey(
        User, related_name='last_plays', null=True, blank=True, on_delete=models.CASCADE)

    next_play_by = models.ForeignKey(
        User, related_name='next_plays', null=True, blank=True, on_delete=models.CASCADE)

    turns_played = models.IntegerField(default=0)

    turn_pointer = models.IntegerField(default=0)

    final_result = models.IntegerField(default=-1)

    def playerslist(self):
        rels = self.players.all().order_by('pk')
        players_str = ''
        for idx, rel in enumerate(rels):
            players_str += f'{rel.player.username} '
        return players_str

    def current_round(self):
        return self.turns_played//4 + 1

    def save(self,  *args, **kwargs):
        if self.pk == None:
            self.next_play_by = self.created_by
        super().save(*args, **kwargs)

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

    round = models.IntegerField(default=0,)

    game_player = models.ForeignKey(
        GamePlayer, null=True, related_name='gameplayers', on_delete=models.CASCADE)

    value_played = models.DecimalField(
        decimal_places=2, default=0, max_digits=12,
    )

    round_result = models.CharField(max_length=500)

    def set_round_result(self, value):
        self.round_result = json.dumps(value)

    def get_round_result(self):
        return json.loads(self.round_result)

    def save(self,  *args, **kwargs):
        if self.pk == None:  # new record
            turns_played = self.__class__.objects.filter(
                game_player__game=self.game_player.game).count()
            self.turn = turns_played + 1
        self.round = self.calc_round(self.turn)
        super().save(*args,  **kwargs)

    def calc_round(self, value):
        _ = value // 4
        if value % 4 > 0 or _ == 0:
            _ += 1
        return _

    def __str__(self):
        return f'{self.turn},{self.game_player.player.username}, {self.value_played}, {self.round_result}'


class TokenForRefresh(models.Model):
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token
