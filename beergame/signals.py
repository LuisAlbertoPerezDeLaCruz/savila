# savila/signals.py

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from accounts.models import User
from .models import Game, GamePlayer, GameTurn, TokenForRefresh, Course, Student
import uuid
from datetime import datetime


@receiver(post_save, sender=Course)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Game)
@receiver(post_save, sender=GamePlayer)
@receiver(post_save, sender=GameTurn)
@receiver(post_delete, sender=Course)
@receiver(post_delete, sender=Student)
@receiver(post_delete, sender=Game)
@receiver(post_delete, sender=GamePlayer)
@receiver(post_delete, sender=GameTurn)
def save_game_player(sender, **kwargs):
    token = str(uuid.uuid4())
    obj = TokenForRefresh.objects.create(token=token)
    TokenForRefresh.objects.exclude(pk=obj.pk).delete()
    return


@receiver(post_save, sender=GameTurn)
def post_save_game_turn(sender, instance, created, **kwargs):

    instance.game_player.last_play_at = datetime.now()

    gameExtraInfoUpdate(created, instance)

    instance.game_player.save()


@receiver(pre_delete, sender=GameTurn)
def pre_delete_game_turn(sender, instance, **kwargs):
    last_instance = GameTurn.objects.last()
    if instance != last_instance:
        pass
        # raise Exception("Can only delete last instance")
    return


@receiver(post_delete, sender=GameTurn)
def post_delete_game_turn(sender, instance, **kwargs):
    last_instance = GameTurn.objects.last()
    gameExtraInfoUpdate(True, last_instance)
    return


def gameExtraInfoUpdate(go_ahead, instance):

    try:
        if go_ahead:
            # A traves del la relacion game_player modifico el objeto game
            # adicionandole loa valores: last_play_at, last_play_by, next_play_by
            # y turns_played

            instance.game_player.game.last_play_at = datetime.now()
            instance.game_player.game.turns_played = instance.turn
            instance.game_player.game.last_play_by = instance.game_player.player

            _ = instance.game_player.game.playerslist().strip().split()
            curr_idx = _.index(instance.game_player.player.username)
            next_idx_ = curr_idx + 1

            if next_idx_ > 3:  # len(_)-1:
                next_idx = 0
            else:
                next_idx = next_idx_

            instance.game_player.game.turn_pointer = next_idx

            next_player = User.objects.get(username=_[next_idx])

            instance.game_player.game.next_play_by = next_player

            rounds_played = instance.game_player.game.turns_played // 4

            if instance.game_player.game.max_turns >= rounds_played:
                instance.game_player.game.status = 'F'

            instance.game_player.game.save()
        else:
            pass
    except Exception as ex:
        pass
