import json
import random
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User

from .models import Game, GamePlayer, GameTurn, Institution, Course, Student, TokenForRefresh
from .forms import NewCourseForm, NewGameForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # import messages
from django.db.models import Q
from .beergame_env import calc_round
import json
import numpy as np


def home(request, institution_pk=None):

    if request.user.is_anonymous:
        institution = Institution.objects.get(name='Global')
        courses = Course.objects.filter(institution=institution)
    elif institution_pk:
        institution = Institution.objects.get(pk=institution_pk)
        courses = Course.objects.filter(
            institution=institution_pk)
    else:
        institution = Institution.objects.get(name='Global')
        courses = Course.objects.filter(institution=institution)

    institutions = Institution.objects.all()

    if not request.user.is_anonymous and not request.user.is_instructor:
        for course in courses:
            student = Student.objects.filter(course=course, user=request.user)
            if student.exists():
                course.student_joined = True
                course.student_status = student[0].get_status_display

    if not request.user.is_anonymous and request.user.is_instructor:
        courses = courses.filter(instructor=request.user)
        return render(request,  'instructor_home.html',
                      {"institution": institution,
                       "institutions": institutions,
                       'courses': courses})
    else:
        return render(request, 'student_home.html',
                      {"institutions": institutions,
                       "institution": institution,
                       'courses': courses})


@login_required
def game_list(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    institution = course.institution
    institutions = Institution.objects.all()

    user_has_active_games = GamePlayer.objects.filter(
        Q(player=request.user, game__status='C') |
        Q(player=request.user, game__status='S')).exists()

    games = Game.objects.filter(course=course).exclude(status='T')

    for game in games:
        game.user_joined = GamePlayer.objects.filter(
            Q(game=game, player=request.user, game__status='C') |
            Q(game=game, player=request.user, game__status='S')).exists()

    return render(request, 'game_list.html',
                  {"institutions": institutions,
                   "institution": institution,
                   'course': course,
                   'games': games,
                   'user_has_active_games': user_has_active_games,
                   })


@login_required
def course_student_list(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    institution = course.institution
    institutions = Institution.objects.all()
    students = Student.objects.filter(
        course=course).order_by('user__first_name')
    return render(request, 'course_student_list.html',
                  {"institutions": institutions,
                   "institution": institution,
                   'course': course,
                   'students': students,
                   })


@login_required
def new_course(request, institution_pk):
    institution = Institution.objects.get(pk=institution_pk)
    institutions = Institution.objects.all()
    course = Course()
    if request.method == 'POST':
        form = NewCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.institution = institution
            course.instructor = request.user
            course.course = course
            course.save()
            courses = Course.objects.filter(instructor=request.user)
            return redirect(f'/beergame/home/{institution.pk}/')
    else:
        form = NewGameForm()
    return render(request,  'new_course.html',
                  {"institution": institution, "institutions": institutions, 'form': form})


@login_required
def new_game(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    institution = course.institution
    institutions = Institution.objects.all()
    game = Game()
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.institution = institution
            game.course = course
            game.save()
            GamePlayer.objects.create(
                game=game,
                player=request.user
            )
        return redirect(f'/beergame/game_list/{course.pk}/')
    else:
        form = NewGameForm()
    return render(request, 'new_game.html', {'course': course, 'institution': institution, 'institutions': institutions, 'game': game, 'form': form})


@login_required
def game(request, pk):
    game = Game.objects.get(pk=pk)
    if game.status == 'F':
        return redirect(f'/beergame/game_finished/{game.pk}/')
    institutions = Institution.objects.all()
    institution = game.institution
    if request.method == 'POST':
        game_player = GamePlayer.objects.get(
            game=game, player=request.user)
        game_turn = createGameTurnObject(request, game_player)
        game = game_turn.game_player.game

    players = GamePlayer.objects.filter(game=pk).order_by('joined_at')

    players_list = list()

    for idx, player in enumerate(players):
        try:
            player.role = pos_description(idx)
            players_list.append(
                f'({player.role}) {player.player.username}')
        except:
            player.role = 'participant'
            players_list.append(
                f'({player.role}) {player.player.username}')

    game_players = GamePlayer.objects.filter(game=game).order_by('pk')

    if request.user.is_instructor:
        roles = [
            'Retailer',
            'Wholesaler',
            'Distributor',
            'Manufacturer'
        ]
        game_turns = GameTurn.objects.filter(
            game_player__game=pk).order_by('turn')

        result_data = [
            [1, 13, 0, 2, 3, 21, 25, 26],
            [4, 14, 17, 5, 6, 22, 25, 26],
            [7, 15, 18, 8, 9, 23, 25, 26],
            [10, 16, 19, 11, 12, 24, 25, 26],
        ]
        for game_turn in game_turns:
            pos = -1
            for idx, player in enumerate(game_players):
                if game_turn.game_player == player:
                    pos = idx
                    break
            game_turn.role = roles[pos]
            game_turn.value_played = int(game_turn.value_played)
            round_result = json.loads(game_turn.round_result)
            game_turn.inventory = round_result[result_data[pos][0]]
            game_turn.backlog = round_result[result_data[pos][1]]
            game_turn.order_client = round_result[result_data[pos][2]]
            game_turn.received_product = round_result[result_data[pos][3]]
            game_turn.to_receive = round_result[result_data[pos][4]]
            game_turn.round_pos_cost = round_result[result_data[pos][5]]
            game_turn.round_cost = round_result[result_data[pos][6]]
            game_turn.cumulative_cost = round_result[result_data[pos][7]]

        view = 'game_instructor_view.html'
    else:
        pos = -1
        for idx, player in enumerate(game_players):
            if player.player == request.user:
                pos = idx
                break
        game_turns = GameTurn.objects.filter(
            game_player__game=pk, game_player__player=request.user).order_by('turn')

        result_data = [
            [1, 13, 0, 2, 3, 25, 26],
            [4, 14, 17, 5, 6, 25, 26],
            [7, 15, 18, 8, 9, 25, 26],
            [10, 16, 19, 11, 12, 25, 26],
        ]

        for game_turn in game_turns:
            game_turn.value_played = int(game_turn.value_played)
            round_result = json.loads(game_turn.round_result)
            game_turn.inventory = round_result[result_data[pos][0]]
            game_turn.backlog = round_result[result_data[pos][1]]
            game_turn.order_client = round_result[result_data[pos][2]]
            game_turn.received_product = round_result[result_data[pos][3]]
            game_turn.to_receive = round_result[result_data[pos][4]]
            game_turn.round_cost = round_result[result_data[pos][5]]
            game_turn.cumulative_cost = round_result[result_data[pos][6]]

        view = 'game_student_view.html'

    return render(request, view, {"game": game,
                                  "players": players,
                                  "players_list": players_list,
                                  "game_turns": game_turns,
                                  "institution": institution,
                                  "institutions": institutions})


@login_required
def game_finished(request, pk):
    institutions = Institution.objects.all()
    game = Game.objects.get(pk=pk)
    institution = game.institution
    players = GamePlayer.objects.filter(game=pk).order_by('joined_at')
    players_list = list()

    for idx, player in enumerate(players):
        try:
            player.role = pos_description(idx)
            players_list.append(
                f'({player.role}) {player.player.username}')
        except:
            player.role = 'participant'
            players_list.append(
                f'({player.role}) {player.player.username}')

    game_players = GamePlayer.objects.filter(game=game).order_by('pk')

    roles = [
        'Retailer',
        'Wholesaler',
        'Distributor',
        'Manufacturer'
    ]
    game_turns = GameTurn.objects.filter(
        game_player__game=pk).order_by('turn')

    list_result = list()
    total_result = 0

    for idx, game_turn in enumerate(game_turns):
        changed_round = (idx+1) % 4 == 0
        if changed_round:
            list_row = list()
            round_result = json.loads(game_turn.round_result)

            list_row.append(game_turn.round)

            # retailer data
            list_row.append(round_result[1])  # Inventory
            list_row.append(round_result[13])  # Backlog

            # wholesaler data
            list_row.append(round_result[4])  # Inventory
            list_row.append(round_result[14])  # Backlog

            # distributor data
            list_row.append(round_result[7])  # Inventory
            list_row.append(round_result[15])  # Backlog

            # manufacturer data
            list_row.append(round_result[10])  # Inventory
            list_row.append(round_result[16])  # Backlog

            # Acumulator
            list_row.append(round_result[26])  # Backlog

            total_result += round_result[25]

            list_result.append(list_row)

    view = 'game_finished_view.html'

    return render(request, view, {"game": game,
                                  "players": players,
                                  "players_list": players_list,
                                  "institution": institution,
                                  "institutions": institutions,
                                  "list_result": list_result,
                                  "total_result": total_result})


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
    return redirect(f'/beergame/game_list/{game.course.pk}/')


@login_required
def joinin_course(request, pk):
    course = Course.objects.get(pk=pk)
    try:
        Student.objects.create(
            course=course,
            user=request.user
        )
        messages.success(
            request, f'{request.user} has joined in {course.name}!')
    except:
        messages.warning(
            request, f'{request.user} is already joined in {course.name}!')
        pass
    courses = Course.objects.all()
    return redirect(f'/beergame/home/{course.institution.pk}/')


def get_token_for_refresh(request):
    data = dict()
    obj = TokenForRefresh.objects.first()
    data['token'] = obj.token
    return JsonResponse(data)


def createGameTurnObject(request, game_player):

    try:
        value_played = float(request.POST.get('played_value', 0))
    except:
        messages.error(
            request, f'Order not valid, please type a number!')
        game_turn = GameTurn.objects.last()
        return game_turn

    game = game_player.game
    bots = game.players.filter(player__is_bot=True)

    game_turn = GameTurn.objects.create(
        game_player=game_player,
        value_played=value_played,
        round_result='')
    game_turn.round_result = calc_round(game_player.game.pk)
    game_turn.save()

    if bots:
        for bot in bots:
            game_turn_bot = GameTurn.objects.create(
                game_player=bot,
                value_played=value_played + np.random.randint(5),
                round_result='')
            game_turn_bot.round_result = calc_round(game_player.game.pk)
            game_turn_bot.save()
        return game_turn_bot

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
    missing = 4 - game.players.count()
    robots = User.objects.filter(is_bot=True)
    for idx in range(missing):
        GamePlayer.objects.create(game=game, player=robots[idx])
    game.status = 'S'
    game.save()
    messages.success(
        request, f'{game.name} started!')
    return redirect(f'/beergame/game/{game.pk}')


def terminate_game(request, pk):
    game = Game.objects.get(pk=pk)
    game.status = 'T'
    game.save()
    messages.success(
        request, f'{game.name} Terminated!')
    return redirect(f'/beergame/game_list/{game.course.pk}/')
