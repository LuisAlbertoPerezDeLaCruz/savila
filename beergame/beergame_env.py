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

    # Aqui comienta el calculo
    # backlog_retailer = 0
    # backlog_wholesaler = 0
    # backlog_distributor = 0
    # backlog_manufacturer = 0

    # state = [0]*13

    # state[0] = current_demand
    # demand_backlog_retailer = current_demand + backlog_retailer
    # sales_retailer = min(demand_backlog_retailer, state[1])
    # backlog_retailer = demand_backlog_retailer - sales_retailer
    # state[13] = backlog_retailer
    # inv_retailer = state[1] - sales_retailer + state[2]
    # state[1] = inv_retailer
    # state[2] = state[3]

    # demand_retailer = action[0]
    # demand_backlog_wholesaler = demand_retailer + backlog_wholesaler
    # sales_wholesaler = min(demand_backlog_wholesaler, state[4])
    # state[3] = sales_wholesaler
    # backlog_wholesaler = demand_backlog_wholesaler - sales_wholesaler
    # state[14] = backlog_wholesaler
    # inv_wholesaler = state[4] - sales_wholesaler + state[5]
    # state[4] = inv_wholesaler
    # state[5] = state[6]

    # demand_wholesaler = action[1]
    # demand_backlog_distributor = demand_wholesaler + backlog_distributor
    # sales_distributor = min(demand_backlog_distributor, state[7])
    # state[6] = sales_distributor
    # backlog_distributor = demand_backlog_distributor - sales_distributor
    # state[15] = backlog_distributor
    # inv_distributor = state[7] - sales_distributor + state[8]
    # state[7] = inv_distributor
    # state[8] = state[9]

    # demand_distributor = action[2]
    # demand_backlog_manufacturer = demand_distributor + backlog_manufacturer
    # sales_manufacturer = min(demand_backlog_manufacturer, state[10])
    # state[9] = sales_manufacturer
    # backlog_manufacturer = demand_backlog_manufacturer - sales_manufacturer
    # state[16] = backlog_manufacturer
    # inv_manufacturer = state[10] - sales_manufacturer + state[11]
    # state[10] = inv_manufacturer
    # state[11] = state[12]

    # state[12] = action[3]

    # turns -= 1
    # curr_turn += 1

    # T_backlog = backlog_retailer + backlog_wholesaler + \
    #     backlog_distributor + backlog_manufacturer
    # T_inv = inv_retailer + inv_wholesaler + inv_distributor + inv_manufacturer

    # reward = -25*T_backlog - 5*T_inv

    # if turns < 0:
    #     done = True
    # else:
    #     done = False

    # info = {}

    # return state, reward, done, info
