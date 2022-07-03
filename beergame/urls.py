from django.urls import path, re_path
from beergame import views as beergame_views

urlpatterns = [
    path('', beergame_views.home, name='home'),
    path('/new_game', beergame_views.new_game, name='new_game'),
]
