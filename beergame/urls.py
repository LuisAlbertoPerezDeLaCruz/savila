from django.urls import path, re_path
from beergame import views as beergame_views

urlpatterns = [
    path('', beergame_views.home, name='home'),
    path('/home', beergame_views.home, name='home'),
    path('/new_game', beergame_views.new_game, name='new_game'),
    path('/joinin_game/<int:pk>/', beergame_views.joinin_game, name='joinin_game'),
]
