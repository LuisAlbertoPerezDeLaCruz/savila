from django.contrib import admin

from .models import Game, GamePlayer, GameTurn, TokenForRefresh, Institution, Course, Student

admin.site.register(Institution)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(GameTurn)
admin.site.register(TokenForRefresh)
