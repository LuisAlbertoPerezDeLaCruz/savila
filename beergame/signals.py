# savila/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, GamePlayer, TokenForRefresh
import uuid


@receiver(post_save, sender=Game)
def save_game(sender, instance, created, **kwargs):
    if created:
        token = str(uuid.uuid4())
        obj = TokenForRefresh.objects.create(token=token)
        TokenForRefresh.objects.exclude(pk=obj.pk).delete()
        pass


@receiver(post_save, sender=GamePlayer)
def save_game_player(sender, instance, created, **kwargs):
    if created:
        token = str(uuid.uuid4())
        obj = TokenForRefresh.objects.create(token=token)
        TokenForRefresh.objects.exclude(pk=obj.pk).delete()
        pass
