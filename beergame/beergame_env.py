# beergame_env.py

import numpy as np
from .models import Game, GameTurn
import random


def calc_round(game_pk):
    previous_round = list()
    current_actions = list()

    game = Game.objects.get(pk=game_pk)

    game_turns = GameTurn.objects.filter(
        game_player__game=game_pk).order_by('-pk')

    previous_round = game_turns[3].round_result

    current_actions = [x.value_played for x in game_turns.reverse()][-4:]

    last_turn = game_turns.reverse().last()

    current_demand = 4 if last_turn.round < 8 else 8
