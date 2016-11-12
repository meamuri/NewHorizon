players = []         # players keys
enemies = dict()     # player_key ---> player_id (his enemy)
game_ids = dict()    # player_key ---> game_id
game_turn = dict()   # player_key ---> TURN_OF_GAME[k]
game_round = dict()  # game_id ---> step of game
maps = dict()        # game_id ---> regions
whose_step = dict()  # game_id ---> player_key
players_id = dict()  # player_key ---> player_id

# current logic: session_key -> game -> whose_step -> game_turn

TURN_OF_GAME = {
    'can_make_move': 0,

    'attack_area': 1,
    'check_round': 2,

    'finished': 3,
}

WHOSE_AREA = {
    'empty': 0,
    'capital_of_second': 1,
    'capital_of_first': 2,
    'area_of_first': 3,
    'area_of_second': 4,
}

# 1. бой за нейтральную
# 2. бой за вражескую:
#   2.1. Оба получили вопросы
#   2.2. Оба ответ:
#       2.2.1. Оба ответили неверно
#       2.2.2. Атакующий ответил неверно
#       2.2.3. Защищающийся ответил неверно
#       2.2.4. Оба ответили верно:
#           2.2.4.1. Вопрос на точность
