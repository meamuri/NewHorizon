# game_turn = dict()   # player_id ---> TURN_OF_GAME[k]
# game_round = dict()  # game_id ---> step of game
# whose_step = dict()  # game_id ---> player_id

players = []         # players id
enemies = dict()     # player_id ---> player_id (his enemy)
game_ids = dict()    # player_id ---> game_id

maps = dict()        # game_id ---> regions
games = dict()       # game_id ---> game

# current logic: session_key -> game -> whose_step -> game_turn

TURN_STATUS = {
    'player_wait': 0,
    'player_can_attack': 1,

    'get_me_enum_question': 10,
    'get_me_accuracy_question': 11,

    'check_enum_quest': 20,
    'check_enum': 21
}


COUNT_OF_ROUNDS = 9


class Game:
    """
    Класс, содержащий информацию о состояниях игры между двумя пользователями
    """
    def __init__(self, player_who_comes_now, player_who_has_waited_some_times):
        self.round = 0

        self.player_comes_now = player_who_comes_now
        self.player_has_waited = player_who_has_waited_some_times

        self.regions = [1, 0, 0, 0,
                        0, 0, 0, 2]
        self.status_for_player = {
            self.player_comes_now: TURN_STATUS['player_can_attack'],
            self.player_has_waited: TURN_STATUS['player_wait']
        }
        self.whose_step = player_who_comes_now

    def key_to_player_id(self, key):
        if key == self.player_comes_now:
            return 1
        elif key == self.player_has_waited:
            return 2
        return -1

    def is_it_his_area(self, player_key, area):
        return self.key_to_player_id(player_key) == self.regions[area]

    def resume_round(self):
        self.whose_step = enemies[self.whose_step]
        self.status_for_player = {
            self.whose_step: TURN_STATUS['player_can_attack'],
            enemies[self.whose_step]: TURN_STATUS['player_wait']
        }
        self.round += 1

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
#
# TURN_OF_GAME = {
#     'can_make_move': 0,
#     'wait_his_opponent': 10,
#
#     'attack_some_area': 1,
#     'attack_neutral_area': 7,
#     'attack_enemy_area': 8,
#
#     'enemy_fight_too': 8,
#     'enemy_attack_me!!!': 9,
#     'accuracy_fight': 3,
#
#     'check_fight_result': 2,
#     'check_accuracy': 4,
#
#     'round_is_over': 5,
#     'finished': 6,
# }
#
