from ast import Try
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Game, GamePlayer, TokenForRefresh
from .forms import NewGameForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # import messages


def home(request):
    games = Game.objects.all()
    return render(request, 'home.html', {"games": games})


@login_required
def new_game(request):
    game = Game()
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.save()
            GamePlayer.objects.create(
                game=game,
                player=request.user
            )
            return redirect('home')
    else:
        form = NewGameForm()
    return render(request, 'new_game.html', {'game': game, 'form': form})


@login_required
def joinin_game(request, pk):
    game = Game.objects.get(pk=pk)
    try:
        GamePlayer.objects.create(
            game=game,
            player=request.user
        )
        messages.success(
            request, f'{request.user} is now playing in {game.name}!')
    except:
        messages.warning(
            request, f'{request.user} is already playing in {game.name}!')
        pass
    games = Game.objects.all()
    return render(request, 'home.html', {"games": games})


def get_token_for_refresh(request):
    data = dict()
    obj = TokenForRefresh.objects.first()
    data['token'] = obj.token
    return JsonResponse(data)
