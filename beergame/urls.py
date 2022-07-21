from django.urls import path, re_path
from beergame import views as beergame_views

urlpatterns = [
    path('', beergame_views.home, name='home'),
    path('home', beergame_views.home, name='home'),
    path('home/<int:institution_pk>/', beergame_views.home, name='home'),
    path('new_game/<int:institution_pk>/',
         beergame_views.new_game, name='new_game'),
    path('game_list/<int:course_pk>/',
         beergame_views.game_list, name='game_list'),
    path('game/<int:pk>/', beergame_views.game, name='game'),
    path('joinin_game/<int:pk>/', beergame_views.joinin_game, name='joinin_game'),
    path('joinin_course/<int:pk>/',
         beergame_views.joinin_course, name='joinin_course'),
    path('start_game/<int:pk>/', beergame_views.start_game, name='start_game'),
    path('ajax/get_token_for_refresh/',
         beergame_views.get_token_for_refresh, name='get_token_for_refresh'),
]
