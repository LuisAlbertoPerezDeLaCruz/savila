# savila/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Game, GamePlayer, GameTurn, TokenForRefresh
import uuid


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


@receiver(post_delete, sender=GameTurn)
def delete_game_turn(sender, **kwargs):
    last_instance = GameTurn.objects.last()
    if last_instance:
        last_instance.save()
    return
