# beergame_env.py

import numpy as np
from .models import Game, GameTurn
import json


def calc_round(game_pk):
    previous_round = list()
    current_actions = list()

    DEM_CON = 0  # Demanda Consumidor

    INV_RET = 1  # Inventario Retailer
    TR1_RET = 2  # Inventario Transito Retailer T1
    TR2_RET = 3  # Inventario Transito Retailer T2

    INV_WHS = 4  # Inventario Wholesaler
    TR1_WHS = 5  # Inventario Transito Wholesaler T1
    TR2_WHS = 6  # Inventario Transito Wholesaler T2

    INV_DIS = 7  # Inventario Distributor
    TR1_DIS = 8  # Inventario Transito Distributor T1
    TR2_DIS = 9  # Inventario Transito Distributor T2

    INV_MNF = 10  # Inventario Manufacturer
    TR1_MNF = 11  # Inventario Transito Manufacturer T1
    TR2_MNF = 12  # Inventario Transito Manufacturer T2

    BCK_RET = 13  # Bqcklog Retailer
    BCK_WHS = 14  # Bqcklog Wholesaler
    BCK_DIS = 15  # Bqcklog Distributor
    BCK_MNF = 16  # Bqcklog Manufacturer

    DEC_RET = 17  # Decision Retailer
    DEC_WHS = 18  # Decision Wholesaler
    DEC_DIS = 19  # Decision Distributor
    DEC_MNF = 20  # Decision Manufacturer

    RES_RET = 21  # Result Retailer
    RES_WHS = 22  # Result Wholesaler
    RES_DIS = 23  # Result Distributor
    RES_MNF = 24  # Result Manufacturer

    TRN_RES = 25  # Resultado Total Turno
    ACM_RES = 26  # Acumulado Resultado

    CUR_ACT_RET = 0  # Current Action Retailer
    CUR_ACT_WHS = 1  # Current Wholesaler
    CUR_ACT_DIS = 2  # Current Distributor
    CUR_ACT_MNF = 3  # Current Manufacturer

    game = Game.objects.get(pk=game_pk)

    game_turns = GameTurn.objects.filter(
        game_player__game=game_pk).order_by('-pk')

    if game.turns_played == 4:
        previous_round = [0]*27

        previous_round[DEM_CON] = 0

        previous_round[INV_RET] = 12
        previous_round[TR1_RET] = 0
        previous_round[TR2_RET] = 0

        previous_round[INV_WHS] = 12
        previous_round[TR1_WHS] = 0
        previous_round[TR2_WHS] = 0

        previous_round[INV_DIS] = 12
        previous_round[TR1_DIS] = 0
        previous_round[TR2_DIS] = 0

        previous_round[INV_MNF] = 12
        previous_round[TR1_MNF] = 0
        previous_round[TR2_MNF] = 0

        previous_round[BCK_RET] = 0
        previous_round[BCK_WHS] = 0
        previous_round[BCK_DIS] = 0
        previous_round[BCK_MNF] = 0

        previous_round[DEC_RET] = 0
        previous_round[DEC_WHS] = 0
        previous_round[DEC_DIS] = 0
        previous_round[DEC_MNF] = 0

        previous_round[RES_RET] = 0
        previous_round[RES_WHS] = 0
        previous_round[RES_DIS] = 0
        previous_round[RES_MNF] = 0

        previous_round[TRN_RES] = 0
        previous_round[ACM_RES] = 0

    else:
        previous_round = json.loads(game_turns[4].round_result)

    current_actions = [x.value_played for x in game_turns.reverse()][-4:]

    last_turn = game_turns.reverse().last()

    current_demand = 4 if last_turn.round < 8 else 8

    state = previous_round

    backlog_retailer = state[BCK_RET]
    backlog_wholesaler = state[BCK_WHS]
    backlog_distributor = state[BCK_DIS]
    backlog_manufacturer = state[BCK_MNF]

    state[DEM_CON] = current_demand
    demand_backlog_retailer = current_demand + backlog_retailer
    sales_retailer = min(demand_backlog_retailer, state[INV_RET])
    backlog_retailer = demand_backlog_retailer - sales_retailer
    state[BCK_RET] = backlog_retailer
    inv_retailer = state[INV_RET] - sales_retailer + state[TR1_RET]
    state[INV_RET] = inv_retailer
    state[TR1_RET] = state[TR2_RET]

    demand_retailer = current_actions[CUR_ACT_RET]
    demand_backlog_wholesaler = demand_retailer + backlog_wholesaler
    sales_wholesaler = min(demand_backlog_wholesaler, state[INV_WHS])
    state[TR2_RET] = sales_wholesaler
    backlog_wholesaler = demand_backlog_wholesaler - sales_wholesaler
    state[BCK_WHS] = backlog_wholesaler
    inv_wholesaler = state[INV_WHS] - sales_wholesaler + state[TR1_WHS]
    state[INV_WHS] = inv_wholesaler
    state[TR1_WHS] = state[TR2_WHS]

    demand_wholesaler = current_actions[CUR_ACT_WHS]
    demand_backlog_distributor = demand_wholesaler + backlog_distributor
    sales_distributor = min(demand_backlog_distributor, state[INV_DIS])
    state[TR2_WHS] = sales_distributor
    backlog_distributor = demand_backlog_distributor - sales_distributor
    state[BCK_DIS] = backlog_distributor
    inv_distributor = state[INV_DIS] - sales_distributor + state[TR1_DIS]
    state[INV_DIS] = inv_distributor
    state[TR1_DIS] = state[TR2_DIS]

    demand_distributor = current_actions[CUR_ACT_DIS]
    demand_backlog_manufacturer = demand_distributor + backlog_manufacturer
    sales_manufacturer = min(demand_backlog_manufacturer, state[INV_MNF])
    state[TR2_DIS] = sales_manufacturer
    backlog_manufacturer = demand_backlog_manufacturer - sales_manufacturer
    state[BCK_MNF] = backlog_manufacturer
    inv_manufacturer = state[INV_MNF] - sales_manufacturer + state[TR1_MNF]
    state[INV_MNF] = inv_manufacturer
    state[TR1_MNF] = state[TR2_MNF]

    state[TR2_MNF] = current_actions[CUR_ACT_MNF]

    state[DEC_RET] = current_actions[CUR_ACT_RET]
    state[DEC_WHS] = current_actions[CUR_ACT_WHS]
    state[DEC_DIS] = current_actions[CUR_ACT_DIS]
    state[DEC_MNF] = current_actions[CUR_ACT_MNF]

    state[RES_RET] = state[BCK_RET]*25 + state[INV_RET]*5
    state[RES_WHS] = state[BCK_WHS]*25 + state[INV_WHS]*5
    state[RES_DIS] = state[BCK_DIS]*25 + state[INV_DIS]*5
    state[RES_MNF] = state[BCK_MNF]*25 + state[INV_MNF]*5

    state[TRN_RES] = state[RES_RET] + \
        state[RES_WHS] + state[RES_DIS] + state[RES_MNF]
    state[ACM_RES] = previous_round[ACM_RES] + state[TRN_RES]

    return [int(x) for x in state]
