players = []         # players id
enemies = dict()     # player_id ---> player_id (his enemy)
game_ids = dict()    # player_id ---> game_id
game_round = dict()  # game_id ---> step of game
game_turn = dict()   # game_id ---> TURN_OF_GAME[k]
maps = dict()        #
whose_step_in_game = dict()

TURN_OF_GAME = {
    'started': 0,
    'attack_some_area': 1,
    'attack_neutral_area': 7,
    'attack_enemy_area': 8,
    'enemy_attack_me!!!': 9,
    'check_fight_result': 2,
    'accuracy_fight': 3,
    'check_accuracy': 4,
    'round_is_over': 5,
    'finished': 6,
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
#
