import random
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Game, GamePlayer, GameTurn, Institution, Course, TokenForRefresh
from .forms import NewGameForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # import messages
from django.db.models import Q
from .beergame_env import calc_round


def home(request, institution_pk=None):

    if request.user.is_anonymous:
        institution = Institution.objects.get(name='Global')
        courses = Course.objects.filter(institution=institution)
        user_has_active_games = False
    elif institution_pk:
        institution = Institution.objects.get(pk=institution_pk)
        courses = Course.objects.filter(
            institution=institution_pk)
        user_has_active_games = GamePlayer.objects.filter(
            Q(player=request.user, game__status='C') | Q(player=request.user, game__status='S')).exists()
    else:
        institution = Institution.objects.get(name='Global')
        courses = Course.objects.filter(institution=institution)
        user_has_active_games = GamePlayer.objects.filter(
            Q(player=request.user, game__status='C') | Q(player=request.user, game__status='S')).exists()

    institutions = Institution.objects.all()

    games = Game.objects.filter(institution=institution)

    if not request.user.is_anonymous and request.user.is_instructor:
        courses = courses.filter(instructor=request.user)
        return render(request,  'instructor_home.html', {"institution": institution, "institutions": institutions, 'courses': courses})
    else:
        return render(request, 'home.html', {"games": games, "user_has_active_games": user_has_active_games, "institutions": institutions, "institution": institution})


@login_required
def new_game(request, institution_pk):
    institutions = Institution.objects.all()
    institution = Institution.objects.get(pk=institution_pk)
    game = Game()
    if request.method == 'POST':
        form = NewGameForm(institution, request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.institution = institution
            game.save()
            GamePlayer.objects.create(
                game=game,
                player=request.user
            )
            return redirect('home')
    else:
        form = NewGameForm(institution)
    return render(request, 'new_game.html', {'game': game, "institutions": institutions, "institution": institution, 'form': form})


@login_required
def game(request, pk):
    game = Game.objects.get(pk=pk)
    if request.method == 'POST':
        game_player = GamePlayer.objects.get(
            game=game, player=request.user)
        game_turn = createGameTurnObject(request, game_player)
        game = game_turn.game_player.game

    players = GamePlayer.objects.filter(game=pk).order_by('joined_at')
    players_list = [
        f'({pos_description(idx)}) {x.player.username}' for idx, x in enumerate(players)]
    game_turns = GameTurn.objects.filter(game_player__game=pk).order_by('turn')
    return render(request, 'game.html', {"game": game,
                                         "players": players,
                                         "players_list": players_list,
                                         "game_turns": game_turns})


def pos_description(pos):
    descriptions = (
        "retailer",
        "wholesaler",
        "distributor",
        "manufacturer"
    )
    return descriptions[pos]


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
    return redirect('home')


def get_token_for_refresh(request):
    data = dict()
    obj = TokenForRefresh.objects.first()
    data['token'] = obj.token
    return JsonResponse(data)


def createGameTurnObject(request, game_player):
    value_played = float(request.POST.get('played_value', 0))

    game_turn = GameTurn.objects.create(
        game_player=game_player,
        value_played=value_played,
        round_result='')

    n = GameTurn.objects.filter(game_player__game=game_player.game).count()

    if n % 4 == 0 and n > 0:
        game_turn.round_result = calc_round(game_player.game.pk)
        game_turn.save()

    return game_turn


def gameTurnResult():
    result = list()
    for i in range(4):
        internal = list()
        for j in range(3):
            n = random.randint(0, 100)
            internal.append(n)
        result.append(internal)
    return result


def start_game(request, pk):
    game = Game.objects.get(pk=pk)
    game.status = 'S'
    game.save()
    messages.success(
        request, f'{game.name} started!')
    return redirect(f'/beergame/game/{game.pk}')
