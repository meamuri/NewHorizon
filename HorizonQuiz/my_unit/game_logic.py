players = []         # players id
enemies = dict()     # player_id ---> player_id (his enemy)
game_ids = dict()    # player_id ---> game_id

maps = dict()        # game_id ---> regions
games = dict()       # game_id ---> game


TURN_STATUS = {
    # Block 1. Game.Status for player
    # эти статусы проверяются гейм центром первыми
    # и либо сразу позволяют направить к контроллеру,
    # либо показывают, что можно обратиться для уточнениям
    # к статусам следующиего блока
    'player_wait_step': 0,
    'player_can_attack': 1,

    'fight_in_progress': 30,  # когда не нужно, чтобы уходил на ветку проверки
    'finished': 31,

    'check_enum_quest': 20,
    'check_accuracy_question': 21,

    # Block 2. Game.GameStatus
    # Теперь нет нужды хранить для каждого игрока, атакует он или защищает и какой тип территории
    # игра сама знает, за что сейчас идет сражение, и смотрит уже только на состояние -- с каким типом вопроса
    # работать и имеет ли право пользователь сейчас обращаться к гейм центру
    'attacked_neutral_area': 70,
    'attacked_area_of_player': 71,
    'attacked_capital': 72,
    'no_status_yet': 75,

    # Block 3. Game.Round state
    # Каждый раунд проходит в несколько этапов,
    # Состояние раунда необходимо для работы
    # attack area и для котроля, какой вопрос выдать следующим
    # просматривается в "attack_area", меняется в этой функции и в fight result
    'get_me_enum_question': 10,
    'get_me_accuracy_question': 11,

    'taken_true_answer': 60,
    'taken_false_answer': 61,
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
        self.game_status = {
            'what_was_attacked': TURN_STATUS['no_status_yet'],
            'area_under_attack': -1,
        }
        self.round_state = {
            self.player_comes_now: TURN_STATUS['get_me_enum_question'],
            self.player_has_waited: TURN_STATUS['get_me_enum_question'],
        }
        self.score = {
            self.player_comes_now: 0,
            self.player_has_waited: 0,
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
          0 - нейтральная
         -1 - вражеская
          1 - игрока
        """
        if self.key_to_player_id(player_key) == self.regions[area]:
            return 1
        elif self.key_to_player_id(his_enemy) == self.regions[area]:
            return -1
        else:
            return 0

    def resume_round(self):
        self.whose_step = enemies[self.whose_step]
        self.status_for_player[self.whose_step] = TURN_STATUS['player_can_attack']
        self.status_for_player[enemies[self.whose_step]] = TURN_STATUS['player_wait_step']
        self.round += 1
        self.step_in_round = 1

    def reg_was_captured(self):
        self.regions[self.game_status['area_under_attack']] = self.key_to_player_id(self.whose_step)

    def resume_part_of_round(self):
        attacker = self.whose_step
        defender = enemies[self.whose_step]
        if self.game_status['what_was_attacked'] == TURN_STATUS['attacked_neutral_area']:
            if self.round_state[attacker] == TURN_STATUS['taken_true_answer']:
                self.reg_was_captured()
            self.resume_round()
            return

        pvp_resume_logic(self, attacker, defender)


def init_round(the_game, area_id, player_key, his_enemy):
    whose = the_game.cmp_whose_this_area(area=area_id, player_key=player_key, his_enemy=his_enemy)
    if whose == 1:
        return {'error': 'this is your area!'}

    res_obj = {'ok': 'ok'}
    the_game.round += 1
    the_game.step_in_round = 1
    the_game.game_status['area_under_attack'] = area_id
    if whose == 0:
        the_game.game_status['what_was_attacked'] = TURN_STATUS['attacked_neutral_area']
        the_game.status_for_player[player_key] = TURN_STATUS['fight_in_progress']
        the_game.status_for_player[his_enemy] = TURN_STATUS['player_wait_step']
        return res_obj

    if area_id == 0 or area_id == len(the_game.regions) - 1:
        the_game.game_status['what_was_attacked'] = TURN_STATUS['attacked_capital']
    else:
        the_game.game_status['what_was_attacked'] = TURN_STATUS['attacked_area_of_player']

    the_game.status_for_player[player_key] = TURN_STATUS['fight_in_progress']
    the_game.status_for_player[his_enemy] = TURN_STATUS['fight_in_progress']
    the_game.round_state[player_key] = TURN_STATUS['get_me_enum_question']
    the_game.round_state[his_enemy] = TURN_STATUS['get_me_enum_question']

    return res_obj


def pvp_resume_logic(the_game, attacker, defender):
    if the_game.round_state[attacker] == TURN_STATUS['taken_false_answer']:
        the_game.resume_round()
        return

    if the_game.round_state[defender] == TURN_STATUS['taken_false_answer']:
        the_game.reg_was_captured()
        the_game.resume_round()
        return

    # Если оба дали верные ответы
    if the_game.status_for_player[attacker] == TURN_STATUS['check_enum_quest']:
        # верные ответы на обычный вопрос -- получаем вопрос на точность
        the_game.round_state[attacker] = TURN_STATUS['get_me_accuracy_question']
        the_game.round_state[defender] = TURN_STATUS['get_me_accuracy_question']

        the_game.status_for_player[attacker] = TURN_STATUS['fight_in_progress']
        the_game.status_for_player[defender] = TURN_STATUS['fight_in_progress']
        return

    # Здесь ситуация, когда неверно ответили оба на перечислимый вопрос
    if the_game.game_status['what_was_attacked'] == TURN_STATUS['attacked_area_of_player']:
        the_game.resume_round()
        return

    # Здесь ситуация, когда неверно ответили оба на вопрос на точность
    # и это атака столицы
    if the_game.step_in_round == 3:
        the_game.resume_round()
    else:
        the_game.round_state += 1
        the_game.round_state[attacker] = TURN_STATUS['get_me_enum_question']
        the_game.round_state[defender] = TURN_STATUS['get_me_enum_question']

        the_game.status_for_player[attacker] = TURN_STATUS['fight_in_progress']
        the_game.status_for_player[defender] = TURN_STATUS['fight_in_progress']
