# savila/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from accounts.models import User
from .models import Game, GamePlayer, GameTurn, TokenForRefresh
import uuid
from datetime import datetime


@receiver(post_save, sender=Game)
@receiver(post_save, sender=GamePlayer)
@receiver(post_save, sender=GameTurn)
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

    # Si el objecto instance no esta creado, entonces el pk en nulo,
    # lo cual quiere decir que estoy creando el objeto y
    # no actualizandolo

    if created:
        # A traves del la relacion game_player modifico el objeto game
        # adicionandole loa valores: last_play_at, last_play_by, next_play_by
        # y turns_played

        instance.game_player.game.last_play_at = datetime.now()
        instance.game_player.game.turns_played = instance.turn
        instance.game_player.game.last_play_by = instance.game_player.player

        _ = instance.game_player.game.playerslist().strip().split()
        curr_idx = _.index(instance.game_player.player.username)
        next_idx_ = curr_idx + 1

        if next_idx_ > len(_)-1:
            next_idx = 0
        else:
            next_idx = next_idx_

        next_player = User.objects.get(username=_[next_idx])

        instance.game_player.game.next_play_by = next_player
        instance.game_player.game.save()
    else:
        # Automaticamente calculo los turns_played, buscando los turns que
        # pertenecen al mismo game
        turns_played = instance.__class__.objects.filter(
            game_player__game=instance.game_player.game).count()
        instance.game_player.game.turns_played = turns_played
        instance.game_player.game.save()

    instance.game_player.save()


@receiver(post_delete, sender=GameTurn)
def delete_game_turn(sender, **kwargs):
    last_instance = GameTurn.objects.last()
    if last_instance:
        last_instance.save()
    return
