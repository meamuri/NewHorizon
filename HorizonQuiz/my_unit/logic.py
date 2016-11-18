game_ids = dict()           # player_key    ---> game_id
games = dict()              # game_id       ---> game
players = []                # keys
player_ids = dict()         # Unique id     ---> player ; для поиска соперника.
enemies = dict()            # player_key    ---> player_key (his enemy)
maps = dict()               # game_id       ---> dict


TURN_OF_GAME = {
    'can_attack': 5,
    'check': 4,
}


AREA_CONDITION = {
    'neutral': 0,
    'our': 1,
    'of_enemy': 2,
    'capital': 3,
}


SITUATION_FOR_PLAYER = {
    'start_game': 10,

    'attack_neutral': 0,
    'attack_enemy': 1,
    'attack_capital': 2,

    'finished_round': 5,
}


class GameMap:
    def __init__(self):
        self.regions = [1, 0, 0, 0, 0, 0, 0, 2]
        self.capitals = [0, 7]  # индексы тех регионов, которые являются столицами

    def set_capitals(self, first=0, second=7):
        self.capitals[0] = first
        self.capitals[1] = second

    def set_regions(self, curr_regions_array):
        self.regions = curr_regions_array

    def region_owner_changed(self, player_id, area_id):
        self.regions[area_id] = player_id

    def is_him_area(self, player_id, area_id):
        return self.regions[area_id] == player_id

    def is_neutral_area(self, area_id):
        return self.regions[area_id] == 0

    def get_area_state(self, area_id):
        if area_id in self.capitals:
            return AREA_CONDITION['capital']
        elif self.regions[area_id] == 0:
            return AREA_CONDITION['neutral']
        else:
            return AREA_CONDITION['of_enemy']


class Game:
    players_parties = dict()  # стороны конфликта, 1 и 2
    members = dict()
    enemies = dict()
    game_map = GameMap()

    def __init__(self, player_key, his_enemy):
        self.player_who_come_later = player_key
        self.player_who_wait_games = his_enemy
        self.players_parties[player_key] = 1
        self.players_parties[his_enemy] = 2
        self.enemies[player_key] = his_enemy
        self.enemies[his_enemy] = player_key
        self.members[1] = player_key
        self.members[2] = his_enemy

        self.round = 0
        self.whose_step = 1
        self.game_turn = TURN_OF_GAME['can_attack']

    def is_your_step(self, player_key):
        """
        Проверка, является ли совершающий запрос пользователь тем игроком, чей чейчас ход
        :param player_key: ключ, идентифицирующий пользователя -- из его запроса
        :return: True, если сейчас действительно должен походить этот пользователь
        """
        return self.whose_step == self.players_parties[player_key]

    def change_map(self, player_who_win, area_id):
        player_id = self.players_parties[player_who_win]
        self.game_map.region_owner_changed(player_id=player_id, area_id=area_id)

    def switch_whose_step(self, key_of_player_whose_step_now):
        self.whose_step = self.enemies[key_of_player_whose_step_now]

    def change_turn(self, it_was_fight):
        if it_was_fight:
            self.game_turn = TURN_OF_GAME['check']
        else:
            self.game_turn = TURN_OF_GAME['can_attack']

    def is_area_him(self, this_player_key, checked_area):
        player_id = self.players_parties[this_player_key]
        return self.game_map.is_him_area(player_id=player_id, area_id=checked_area)

    def is_neutral_area(self, checked_area):
        return self.game_map.is_neutral_area(area_id=checked_area)

    def get_area_state(self, area_id):
        return self.game_map.get_area_state(area_id)