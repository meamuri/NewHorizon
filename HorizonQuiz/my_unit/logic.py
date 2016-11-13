from HorizonQuiz.my_unit.model_unit import Region

game_ids = dict()           # player_key    ---> game_id
games = dict()              # game_id       ---> game
players = []                # keys
player_ids = dict()         # Unique id     ---> player ; для поиска соперника.
enemies = dict()            # player_key    ---> player_key (his enemy)

TURN_OF_GAME = {
    'round_start': 0,
    'player_can_make_move': 1,
    'user_want_take_answer_and_check': 2,
    'round_is_over': 3,
}


class GameMap:
    regions = []
    capitals = [0, 0]  # индексы тех регионов, которые являются столицами

    def set_capitals(self, first, second):
        self.capitals[0] = first
        self.capitals[1] = second

    def set_regions(self, curr_map):
        self.regions = curr_map


class Game:
    players_parties = dict()  # стороны конфликта, 1 и 2
    round = 0
    game_turn = dict()
    game_round = 0

    def __init__(self, player_key, his_enemy):
        self.player_who_come_later = player_key
        self.player_who_wait_games = his_enemy
        self.players_parties[player_key] = 1
        self.players_parties[his_enemy] = 2
        self.whose_step = player_ids[player_key]  # ход игрока 1, (который пришел позже)
        self.game_map = Region()
        self.game_turn[self.round] = TURN_OF_GAME['round_start']
