from django.contrib import admin

from .models import Game, GamePlayer, TokenForRefresh


admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(TokenForRefresh)
