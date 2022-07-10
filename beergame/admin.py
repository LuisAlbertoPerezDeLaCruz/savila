from django.contrib import admin

from .models import Game, GamePlayer, GameTurn, TokenForRefresh


admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(GameTurn)
admin.site.register(TokenForRefresh)
