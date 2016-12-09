players = []         # players id
enemies = dict()     # player_id ---> player_id (his enemy)
game_ids = dict()    # player_id ---> game_id

maps = dict()        # game_id ---> regions
games = dict()       # game_id ---> game

# current logic: session_key -> game -> whose_step -> game_turn

TURN_STATUS = {

    # Block 1. Game.Status for player
    # эти статусы проверяются гейм центром первыми
    # и либо сразу позволяют направить к контроллеру,
    # либо показывают, что можно обратиться для уточнениям
    # к статусам следующиего блока

    'player_wait_step': 0,
    'player_can_attack': 1,

    'fight_in_progress': 30,
    'finished': 31,

    'check_enum_quest': 20,
    'check_accuracy_question': 21,

    # Block 2. Request session status
    # статусы ниже присваваются единожды на каждом раунде, когда
    # игрок, чей сейчас ход, впервые обращается в геймцентр, имея стутс 'can attack'

    'attack_neutral': 40,
    'def_neutral': 41,  # мб не нужен

    'attack_enemy': 45,
    'defence_against_enemy': 46,

    'attack_capital': 50,
    'defence_capital': 51,

    'have_not_round_status': 55,

    # Block 3. Game.Round state
    # Каждый раунд проходит в несколько этапов,
    # Состояние раунда необходимо для работы
    # attack area и для котроля, какой вопрос выдать следующим
    # просматривается в "attack_area", меняется в этой функции и в fight result

    'get_me_enum_question': 10,
    'get_me_accuracy_question': 11,

    'taken_true_answer': 60,
    'taken_false_answer': 61,

    'have_not_round_state': 65,

    # Block 4. Game.GameStatus!!
    # Теперь нет нужды хранит для каждого игрока, атакует он или защищает и какой тип территории
    # игра сама знает, за что сейчас идет сражение, и смотрит уже только на состояние -- с каким типом вопроса
    # работать и имеет ли право пользователь сейчас обращаться к гейм центру

    'attacked_neutral_area': 70,
    'attacked_area_of_player': 70,
    'attacked_capital': 70,
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
            self.player_has_waited: TURN_STATUS['player_wait_step'],
        }
        self.round_status = {  # атака или защита нейтральной/ вражеской/ столичной территории
            self.player_comes_now: TURN_STATUS['player_wait_step'],
            self.player_has_waited: TURN_STATUS['player_wait_step'],
        }
        self.round_state = {
            'step': 1,
            self.player_comes_now: TURN_STATUS['get_me_enum_question'],
            self.player_has_waited: TURN_STATUS['get_me_enum_question'],
        }
        self.step_in_round = 0
        self.whose_step = player_who_comes_now

    def key_to_player_id(self, key):
        if key == self.player_comes_now:
            return 1
        elif key == self.player_has_waited:
            return 2
        return -1

    def cmp_whose_this_area(self, area, player_key, his_enemy):
        """

        :param player_key:
        :param area:
        :param his_enemy:
        :return:
         0  - нейтральная
         -1 - вражеская
         1  - игрока
        """
        if self.key_to_player_id(player_key) == self.regions[area]:
            return 1
        elif self.key_to_player_id(his_enemy) == self.regions[area]:
            return -1
        else:
            return 0

    def resume_round(self):
        self.whose_step = enemies[self.whose_step]
        self.status_for_player = {
            self.whose_step: TURN_STATUS['player_can_attack'],
            enemies[self.whose_step]: TURN_STATUS['player_wait']
        }
        self.round += 1


def resume_round(the_game, player_key, his_enemy):
    pass


def init_round(the_game, area_id, player_key, his_enemy):
    whose = the_game.cmp_whose_this_area(area=area_id, player_key=player_key, his_enemy=his_enemy)
    if whose == 1:
        return {'error': 'this is your area!'}

    the_game.step_in_round = 0
    res_obj = {'ok': 'ok'}

    if whose == 0:
        the_game.round_status[player_key] = TURN_STATUS['attack_neutral']
        return res_obj
        # the_game.round_status[player_key] = game_logic.TURN_STATUS['attack_neutral']

    if area_id == 0 or area_id == len(the_game.regions) - 1:
        the_game.round_status[player_key] = TURN_STATUS['attack_capital']
        the_game.round_status[his_enemy] = TURN_STATUS['defence_capital']
    else:
        the_game.round_status[player_key] = TURN_STATUS['attack_enemy']
        the_game.round_status[his_enemy] = TURN_STATUS['defence_against_enemy']

    the_game.round_state[player_key] = TURN_STATUS['get_me_enum_question']
    the_game.round_state[his_enemy] = TURN_STATUS['get_me_enum_question']

    return res_obj

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
